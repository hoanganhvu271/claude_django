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

from .ml_models import ImprovedDiseasePredictionNetwork, MultiTaskLoss, FocalLoss

from .knowledge_generator import MedicalKnowledgeGenerator
from .symptom_extractor import SymptomExtractor

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
            'early_stopping_patience': 15,
            'hidden_dims': [512, 256, 128],
            'dropout_rate': 0.3,
            'use_focal_loss': True,
            'use_multitask': False  # Set to True if you want multi-task learning
        }
        
        # Load existing model if available
        self.load_model()
    
    def prepare_training_data(self) -> Tuple[np.ndarray, np.ndarray, List[str], List[str]]:
        """Prepare training data from database with data augmentation"""
        from .models import Disease, Symptom, DiseaseSymptom
    
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
            
            # Split data with fallback for stratification
            try:
                # Try stratified split first
                X_train, X_test, y_train, y_test = train_test_split(
                    X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
                )
                logger.info("Using stratified train-test split")
            except ValueError as e:
                # Fallback to regular split if stratification fails
                logger.warning(f"Stratified split failed: {e}. Using regular split.")
                X_train, X_test, y_train, y_test = train_test_split(
                    X_scaled, y_encoded, test_size=0.2, random_state=42
                )

            # Create model
            num_symptoms = X.shape[1]
            num_diseases = len(disease_names)
            
            self.model = ImprovedDiseasePredictionNetwork(
                num_symptoms=num_symptoms,
                num_diseases=num_diseases,
                hidden_dims=self.training_config['hidden_dims'],
                use_attention=True,
                use_residual=True,
                dropout_rate=self.training_config['dropout_rate']
            ).to(self.device)
            
            # Setup loss function
            if self.training_config['use_focal_loss']:
                criterion = FocalLoss(alpha=1.0, gamma=2.0)
            else:
                criterion = nn.CrossEntropyLoss()
            
            # Setup optimizer with weight decay
            optimizer = optim.AdamW(
                self.model.parameters(), 
                lr=self.training_config['learning_rate'],
                weight_decay=1e-4
            )
            
            # Learning rate scheduler
            scheduler = optim.lr_scheduler.CosineAnnealingLR(
                optimizer, 
                T_max=self.training_config['epochs'],
                eta_min=1e-6
            )
            
            # Create data loaders
            train_dataset = TensorDataset(
                torch.FloatTensor(X_train),
                torch.LongTensor(y_train)
            )
            train_loader = DataLoader(
                train_dataset, 
                batch_size=self.training_config['batch_size'], 
                shuffle=True
            )
            
            # Training loop
            best_accuracy = 0
            patience_counter = 0
            train_losses = []
            val_accuracies = []
            
            for epoch in range(self.training_config['epochs']):
                self.model.train()
                epoch_loss = 0
                correct_predictions = 0
                total_predictions = 0
                
                for batch_symptoms, batch_diseases in train_loader:
                    batch_symptoms = batch_symptoms.to(self.device)
                    batch_diseases = batch_diseases.to(self.device)
                    
                    # Forward pass - FIX: Use correct output format
                    outputs = self.model(batch_symptoms)
                    disease_logits = outputs['disease_logits']  # Get from dictionary
                    
                    loss = criterion(disease_logits, batch_diseases)
                    
                    # Backward pass
                    optimizer.zero_grad()
                    loss.backward()
                    
                    # Gradient clipping
                    torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
                    
                    optimizer.step()
                    
                    epoch_loss += loss.item()
                    
                    # Calculate accuracy
                    _, predicted = torch.max(disease_logits, 1)
                    correct_predictions += (predicted == batch_diseases).sum().item()
                    total_predictions += batch_diseases.size(0)
                
                # Step scheduler
                scheduler.step()
                
                avg_loss = epoch_loss / len(train_loader)
                train_accuracy = correct_predictions / total_predictions
                train_losses.append(avg_loss)
                
                # Validation
                if epoch % 5 == 0 or epoch == self.training_config['epochs'] - 1:
                    val_accuracy = self._evaluate_model(X_test, y_test)
                    val_accuracies.append(val_accuracy)
                    
                    current_lr = scheduler.get_last_lr()[0]
                    logger.info(
                        f"Epoch {epoch:3d}: Loss = {avg_loss:.4f}, "
                        f"Train Acc = {train_accuracy:.4f}, Val Acc = {val_accuracy:.4f}, "
                        f"LR = {current_lr:.6f}"
                    )
                    
                    if val_accuracy > best_accuracy:
                        best_accuracy = val_accuracy
                        patience_counter = 0
                        self.save_model()
                        logger.info(f"New best model saved! Accuracy: {best_accuracy:.4f}")
                    else:
                        patience_counter += 1
                    
                    if patience_counter >= self.training_config['early_stopping_patience']:
                        logger.info(f"Early stopping at epoch {epoch}")
                        break
            
            # Final evaluation
            final_accuracy = self._evaluate_model(X_test, y_test)
            logger.info(f"Training completed. Final accuracy: {final_accuracy:.4f}")
            
            # Generate detailed classification report
            self._generate_classification_report(X_test, y_test, disease_names)
            
            # Save model metadata
            metadata = {
                'num_symptoms': num_symptoms,
                'num_diseases': num_diseases,
                'symptom_names': symptom_names,
                'disease_names': disease_names,
                'final_accuracy': final_accuracy,
                'best_accuracy': best_accuracy,
                'training_samples': len(X_train),
                'test_samples': len(X_test),
                'epochs_trained': epoch + 1,
                'training_config': self.training_config
            }
            
            import json
            with open(self.metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            logger.error(f"Training failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def _evaluate_model(self, X_test: np.ndarray, y_test: np.ndarray) -> float:
        """Evaluate model on test data"""
        self.model.eval()
        
        with torch.no_grad():
            X_test_tensor = torch.FloatTensor(X_test).to(self.device)
            y_test_tensor = torch.LongTensor(y_test).to(self.device)
            
            # FIX: Use correct output format
            outputs = self.model(X_test_tensor)
            disease_logits = outputs['disease_logits']
            
            _, predicted = torch.max(disease_logits, 1)
            accuracy = (predicted == y_test_tensor).float().mean().item()
            
        return accuracy
    
    def _generate_classification_report(self, X_test: np.ndarray, y_test: np.ndarray, disease_names: List[str]):
        """Generate detailed classification report"""
        self.model.eval()
        
        with torch.no_grad():
            X_test_tensor = torch.FloatTensor(X_test).to(self.device)
            outputs = self.model(X_test_tensor)
            disease_logits = outputs['disease_logits']
            
            _, predicted = torch.max(disease_logits, 1)
            predicted_np = predicted.cpu().numpy()
            
            # Generate classification report
            report = classification_report(
                y_test, predicted_np, 
                target_names=disease_names, 
                output_dict=True
            )
            
            logger.info("Classification Report:")
            logger.info(classification_report(y_test, predicted_np, target_names=disease_names))
            
            # Save report
            report_path = os.path.join(self.model_dir, 'classification_report.json')
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
    
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
                
                # FIX: Use correct output format
                outputs = self.model(input_tensor)
                disease_logits = outputs['disease_logits']
                confidence_score = outputs['confidence']
                attention_weights = outputs.get('attention_weights')
                
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
                        'overall_confidence': confidence_score[0].item() if confidence_score is not None else None,
                        'attention_weights': attention_weights.cpu().numpy().tolist() if attention_weights is not None else None
                    })
                
                return results
                
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            import traceback
            logger.error(traceback.format_exc())
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
                self.model = ImprovedDiseasePredictionNetwork(
                    num_symptoms=num_symptoms,
                    num_diseases=num_diseases,
                    hidden_dims=self.training_config['hidden_dims'],
                    use_attention=True,
                    use_residual=True,
                    dropout_rate=self.training_config['dropout_rate']
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
            'device': str(self.device),
            'model_type': 'ImprovedDiseasePredictionNetwork'
        }
        
        if os.path.exists(self.metadata_path):
            import json
            with open(self.metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                info.update(metadata)
        
        # Add model complexity info if model is loaded
        if self.model is not None:
            total_params = sum(p.numel() for p in self.model.parameters())
            trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
            
            info.update({
                'total_parameters': total_params,
                'trainable_parameters': trainable_params,
                'model_size_mb': total_params * 4 / (1024 * 1024)  # Approximate size in MB
            })
        
        return info
    
    def interpret_prediction(self, symptoms_text: str) -> Dict:
        """Get detailed interpretation of prediction"""
        if self.model is None:
            return {'error': 'Model not available'}
        
        try:
            # Extract symptoms
            extracted_symptoms = self.symptom_extractor.extract_symptoms(symptoms_text)
            
            if not extracted_symptoms:
                return {'error': 'No symptoms detected'}
            
            # Create symptom vector
            symptom_vector = self._create_symptom_vector(extracted_symptoms)
            
            if symptom_vector is None:
                return {'error': 'Cannot process symptoms'}
            
            # Scale and predict
            symptom_vector_scaled = self.scaler.transform([symptom_vector])
            input_tensor = torch.FloatTensor(symptom_vector_scaled).to(self.device)
            
            # Get model interpretation
            interpretation = self.model.interpret_prediction(input_tensor)
            
            return {
                'extracted_symptoms': extracted_symptoms,
                'symptom_vector': symptom_vector.tolist(),
                'interpretation': interpretation
            }
            
        except Exception as e:
            logger.error(f"Interpretation error: {e}")
            return {'error': str(e)}