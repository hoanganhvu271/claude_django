import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import os
from typing import List, Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class MLEngine:
    """Main Machine Learning Engine for Disease Prediction"""
    
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Using device: {self.device}")
        
        # Models and encoders
        self.model = None
        self.symptom_encoder = LabelEncoder()
        self.disease_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        
        # Components
        self.symptom_extractor = SymptomExtractor()
        self.knowledge_generator = MedicalKnowledgeGenerator()
        
        # Model files
        self.model_dir = 'models'
        os.makedirs(self.model_dir, exist_ok=True)
        
        self.model_path = os.path.join(self.model_dir, 'disease_prediction_model.pth')
        self.encoders_path = os.path.join(self.model_dir, 'encoders.pkl')
        self.metadata_path = os.path.join(self.model_dir, 'model_metadata.json')
        
        # Training parameters
        self.training_config = {
            'batch_size': 32,
            'learning_rate': 0.001,
            'epochs': 100,
            'early_stopping_patience': 10,
            'hidden_dims': [512, 256, 128],
            'dropout_rate': 0.3
        }
        
        # Load existing model if available
        self.load_model()
    
    def prepare_training_data(self) -> Tuple[np.ndarray, np.ndarray, List[str], List[str]]:
        """Prepare training data from database"""
        from .models import Disease, Symptom, DiseaseSymptom
        
        diseases = list(Disease.objects.filter(is_active=True))
        symptoms = list(Symptom.objects.all())
        
        if len(diseases) < 2 or len(symptoms) < 3:
            raise ValueError(f"Insufficient data: {len(diseases)} diseases, {len(symptoms)} symptoms")
        
        # Create symptom-disease matrix
        data_matrix = []
        disease_labels = []
        
        for disease in diseases:
            disease_symptoms = DiseaseSymptom.objects.filter(disease=disease)
            
            # Create symptom vector for this disease
            symptom_vector = np.zeros(len(symptoms))
            
            for ds in disease_symptoms:
                try:
                    symptom_idx = symptoms.index(ds.symptom)
                    # Use probability * importance as the feature value
                    symptom_vector[symptom_idx] = ds.probability * ds.importance
                except ValueError:
                    continue
            
            # Only add if has symptoms
            if np.sum(symptom_vector) > 0:
                data_matrix.append(symptom_vector)
                disease_labels.append(disease.name)
        
        if len(data_matrix) == 0:
            raise ValueError("No valid disease-symptom relationships found")
        
        # Convert to numpy arrays
        X = np.array(data_matrix)
        y = np.array(disease_labels)
        
        # Get feature and label names
        symptom_names = [s.name for s in symptoms]
        disease_names = list(set(disease_labels))
        
        logger.info(f"Prepared training data: {X.shape[0]} samples, {X.shape[1]} symptoms, {len(disease_names)} diseases")
        
        return X, y, symptom_names, disease_names
    
    def train_model(self) -> bool:
        """Train the disease prediction model"""
        try:
            logger.info("Starting model training...")
            
            # Prepare data
            X, y, symptom_names, disease_names = self.prepare_training_data()
            
            # Encode labels
            y_encoded = self.disease_encoder.fit_transform(y)
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
            )
            
            # Create model
            num_symptoms = X.shape[1]
            num_diseases = len(disease_names)
            
            self.model = DiseasePredictionNetwork(
                num_symptoms=num_symptoms,
                num_diseases=num_diseases,
                hidden_dims=self.training_config['hidden_dims']
            ).to(self.device)
            
            # Training setup
            criterion = nn.CrossEntropyLoss()
            optimizer = optim.Adam(self.model.parameters(), lr=self.training_config['learning_rate'])
            
            # Create data loaders
            train_dataset = TensorDataset(
                torch.FloatTensor(X_train),
                torch.LongTensor(y_train)
            )
            train_loader = DataLoader(train_dataset, batch_size=self.training_config['batch_size'], shuffle=True)
            
            # Training loop
            best_accuracy = 0
            patience_counter = 0
            train_losses = []
            
            for epoch in range(self.training_config['epochs']):
                self.model.train()
                epoch_loss = 0
                
                for batch_symptoms, batch_diseases in train_loader:
                    batch_symptoms = batch_symptoms.to(self.device)
                    batch_diseases = batch_diseases.to(self.device)
                    
                    # Forward pass
                    disease_logits, attention_weights, confidence = self.model(batch_symptoms)
                    loss = criterion(disease_logits, batch_diseases)
                    
                    # Backward pass
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()
                    
                    epoch_loss += loss.item()
                
                avg_loss = epoch_loss / len(train_loader)
                train_losses.append(avg_loss)
                
                # Validation
                if epoch % 10 == 0:
                    accuracy = self._evaluate_model(X_test, y_test)
                    logger.info(f"Epoch {epoch}: Loss = {avg_loss:.4f}, Accuracy = {accuracy:.4f}")
                    
                    if accuracy > best_accuracy:
                        best_accuracy = accuracy
                        patience_counter = 0
                        self.save_model()
                    else:
                        patience_counter += 1
                    
                    if patience_counter >= self.training_config['early_stopping_patience']:
                        logger.info(f"Early stopping at epoch {epoch}")
                        break
            
            # Final evaluation
            final_accuracy = self._evaluate_model(X_test, y_test)
            logger.info(f"Training completed. Final accuracy: {final_accuracy:.4f}")
            
            # Save model metadata
            metadata = {
                'num_symptoms': num_symptoms,
                'num_diseases': num_diseases,
                'symptom_names': symptom_names,
                'disease_names': disease_names,
                'final_accuracy': final_accuracy,
                'training_samples': len(X_train),
                'test_samples': len(X_test)
            }
            
            import json
            with open(self.metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            logger.error(f"Training failed: {e}")
            return False
    
    def _evaluate_model(self, X_test: np.ndarray, y_test: np.ndarray) -> float:
        """Evaluate model on test data"""
        self.model.eval()
        
        with torch.no_grad():
            X_test_tensor = torch.FloatTensor(X_test).to(self.device)
            y_test_tensor = torch.LongTensor(y_test).to(self.device)
            
            disease_logits, _, _ = self.model(X_test_tensor)
            _, predicted = torch.max(disease_logits, 1)
            
            accuracy = (predicted == y_test_tensor).float().mean().item()
            
        return accuracy
    
    def predict_disease(self, symptoms_text: str) -> List[Dict]:
        """Predict diseases from symptom text"""
        if self.model is None:
            return [{'disease': 'Model not trained', 'confidence': 0.0, 'error': 'Model not available'}]
        
        try:
            # Extract symptoms using NLP
            extracted_symptoms = self.symptom_extractor.extract_symptoms(symptoms_text)
            
            if not extracted_symptoms:
                return [{'disease': 'No symptoms detected', 'confidence': 0.0, 'extracted_symptoms': []}]
            
            # Create symptom vector
            symptom_vector = self._create_symptom_vector(extracted_symptoms)
            
            if symptom_vector is None:
                return [{'disease': 'Cannot process symptoms', 'confidence': 0.0}]
            
            # Scale symptom vector
            symptom_vector_scaled = self.scaler.transform([symptom_vector])
            
            # Predict
            self.model.eval()
            with torch.no_grad():
                input_tensor = torch.FloatTensor(symptom_vector_scaled).to(self.device)
                disease_logits, attention_weights, confidence_score = self.model(input_tensor)
                
                # Get probabilities
                probabilities = torch.softmax(disease_logits, dim=1)
                
                # Get top predictions
                top_probs, top_indices = torch.topk(probabilities, min(5, len(self.disease_encoder.classes_)))
                
                results = []
                for i, (prob, idx) in enumerate(zip(top_probs[0], top_indices[0])):
                    disease_name = self.disease_encoder.inverse_transform([idx.item()])[0]
                    
                    results.append({
                        'disease': disease_name,
                        'confidence': prob.item(),
                        'rank': i + 1,
                        'extracted_symptoms': [s['name'] for s in extracted_symptoms],
                        'symptom_attention': attention_weights[0].cpu().numpy().tolist(),
                        'overall_confidence': confidence_score[0].item()
                    })
                
                return results
                
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return [{'disease': 'Prediction failed', 'confidence': 0.0, 'error': str(e)}]
    
    def _create_symptom_vector(self, extracted_symptoms: List[Dict]) -> Optional[np.ndarray]:
        """Create symptom vector from extracted symptoms"""
        try:
            from .models import Symptom
            all_symptoms = list(Symptom.objects.all())
            
            if not all_symptoms:
                return None
            
            symptom_vector = np.zeros(len(all_symptoms))
            
            for extracted in extracted_symptoms:
                symptom_name = extracted['name']
                severity = extracted.get('severity', 'moderate')
                
                # Find matching symptom in database
                matching_symptom = None
                for symptom in all_symptoms:
                    if symptom.name.lower() == symptom_name.lower():
                        matching_symptom = symptom
                        break
                
                if matching_symptom:
                    symptom_idx = all_symptoms.index(matching_symptom)
                    
                    # Weight by severity
                    severity_weights = {'mild': 0.5, 'moderate': 1.0, 'severe': 1.5}
                    weight = severity_weights.get(severity, 1.0)
                    
                    symptom_vector[symptom_idx] = weight
            
            return symptom_vector if np.sum(symptom_vector) > 0 else None
            
        except Exception as e:
            logger.error(f"Error creating symptom vector: {e}")
            return None
    
    def save_model(self):
        """Save trained model and encoders"""
        try:
            if self.model:
                torch.save(self.model.state_dict(), self.model_path)
            
            # Save encoders and scaler
            encoders = {
                'disease_encoder': self.disease_encoder,
                'scaler': self.scaler
            }
            
            with open(self.encoders_path, 'wb') as f:
                pickle.dump(encoders, f)
            
            logger.info("Model saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving model: {e}")
    
    def load_model(self):
        """Load trained model and encoders"""
        try:
            # Load encoders
            if os.path.exists(self.encoders_path):
                with open(self.encoders_path, 'rb') as f:
                    encoders = pickle.load(f)
                    self.disease_encoder = encoders['disease_encoder']
                    self.scaler = encoders['scaler']
            
            # Load model metadata
            if os.path.exists(self.metadata_path):
                import json
                with open(self.metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                num_symptoms = metadata['num_symptoms']
                num_diseases = metadata['num_diseases']
                
                # Create and load model
                self.model = DiseasePredictionNetwork(
                    num_symptoms=num_symptoms,
                    num_diseases=num_diseases,
                    hidden_dims=self.training_config['hidden_dims']
                ).to(self.device)
                
                if os.path.exists(self.model_path):
                    self.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
                    logger.info("Model loaded successfully")
                
        except Exception as e:
            logger.warning(f"Could not load model: {e}")
    
    def get_model_info(self) -> Dict:
        """Get information about the current model"""
        info = {
            'model_loaded': self.model is not None,
            'model_path_exists': os.path.exists(self.model_path),
            'encoders_path_exists': os.path.exists(self.encoders_path),
            'device': str(self.device)
        }
        
        if os.path.exists(self.metadata_path):
            import json
            with open(self.metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                info.update(metadata)
        
        return info