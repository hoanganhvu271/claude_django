# chatbot_service_app/ml_models.py - Improved Version
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import List, Tuple, Dict

class ResidualBlock(nn.Module):
    """Residual block for better gradient flow"""
    
    def __init__(self, input_dim: int, hidden_dim: int, dropout: float = 0.3):
        super(ResidualBlock, self).__init__()
        
        self.linear1 = nn.Linear(input_dim, hidden_dim)
        self.linear2 = nn.Linear(hidden_dim, input_dim)
        self.batch_norm1 = nn.BatchNorm1d(hidden_dim)
        self.batch_norm2 = nn.BatchNorm1d(input_dim)
        self.dropout = nn.Dropout(dropout)
        self.activation = nn.GELU()
        
        # Skip connection projection if dimensions don't match
        self.skip_connection = nn.Identity() if input_dim == hidden_dim else nn.Linear(input_dim, input_dim)
        
    def forward(self, x):
        residual = self.skip_connection(x)
        
        out = self.linear1(x)
        out = self.batch_norm1(out)
        out = self.activation(out)
        out = self.dropout(out)
        
        out = self.linear2(out)
        out = self.batch_norm2(out)
        
        # Add residual connection
        out = out + residual
        out = self.activation(out)
        
        return out

class AttentionModule(nn.Module):
    """Self-attention module for symptom relationships"""
    
    def __init__(self, input_dim: int, num_heads: int = 8):
        super(AttentionModule, self).__init__()
        
        self.input_dim = input_dim
        self.num_heads = num_heads
        self.head_dim = input_dim // num_heads
        
        assert input_dim % num_heads == 0, "input_dim must be divisible by num_heads"
        
        self.query = nn.Linear(input_dim, input_dim)
        self.key = nn.Linear(input_dim, input_dim)
        self.value = nn.Linear(input_dim, input_dim)
        self.output_proj = nn.Linear(input_dim, input_dim)
        
        self.dropout = nn.Dropout(0.1)
        self.layer_norm = nn.LayerNorm(input_dim)
        
    def forward(self, x):
        batch_size, seq_len = x.size(0), 1
        residual = x
        
        # Reshape for attention (add sequence dimension)
        x = x.unsqueeze(1)  # [batch, 1, input_dim]
        
        # Linear transformations
        Q = self.query(x).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        K = self.key(x).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        V = self.value(x).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        
        # Scaled dot-product attention
        scores = torch.matmul(Q, K.transpose(-2, -1)) / np.sqrt(self.head_dim)
        attention_weights = F.softmax(scores, dim=-1)
        attention_weights = self.dropout(attention_weights)
        
        context = torch.matmul(attention_weights, V)
        
        # Concatenate heads
        context = context.transpose(1, 2).contiguous().view(batch_size, seq_len, self.input_dim)
        
        # Output projection
        output = self.output_proj(context)
        output = output.squeeze(1)  # Remove sequence dimension
        
        # Residual connection and layer norm
        output = self.layer_norm(output + residual)
        
        return output, attention_weights.squeeze()

class ImprovedDiseasePredictionNetwork(nn.Module):
    """Enhanced Neural Network for Disease Prediction with Advanced Features"""
    
    def __init__(self, 
                 num_symptoms: int, 
                 num_diseases: int, 
                 hidden_dims: List[int] = [512, 256, 128],
                 use_attention: bool = True,
                 use_residual: bool = True,
                 dropout_rate: float = 0.3,
                 use_batch_norm: bool = True):
        super(ImprovedDiseasePredictionNetwork, self).__init__()
        
        self.num_symptoms = num_symptoms
        self.num_diseases = num_diseases
        self.use_attention = use_attention
        self.use_residual = use_residual
        
        # Input embedding and projection
        self.input_embedding = nn.Sequential(
            nn.Linear(num_symptoms, hidden_dims[0]),
            nn.BatchNorm1d(hidden_dims[0]) if use_batch_norm else nn.Identity(),
            nn.GELU(),
            nn.Dropout(dropout_rate)
        )
        
        # Symptom importance weighting
        self.symptom_weights = nn.Parameter(torch.ones(num_symptoms))
        
        # Multi-head attention for symptom relationships
        if use_attention:
            self.symptom_attention = AttentionModule(hidden_dims[0], num_heads=8)
        
        # Residual blocks or regular layers
        self.feature_layers = nn.ModuleList()
        
        for i in range(len(hidden_dims) - 1):
            if use_residual and hidden_dims[i] == hidden_dims[i + 1]:
                # Use residual block when dimensions match
                self.feature_layers.append(
                    ResidualBlock(hidden_dims[i], hidden_dims[i] * 2, dropout_rate)
                )
            else:
                # Regular layer
                self.feature_layers.append(
                    nn.Sequential(
                        nn.Linear(hidden_dims[i], hidden_dims[i + 1]),
                        nn.BatchNorm1d(hidden_dims[i + 1]) if use_batch_norm else nn.Identity(),
                        nn.GELU(),
                        nn.Dropout(dropout_rate)
                    )
                )
        
        # Disease-specific feature extraction
        self.disease_specific_layers = nn.ModuleList([
            nn.Sequential(
                nn.Linear(hidden_dims[-1], hidden_dims[-1] // 2),
                nn.GELU(),
                nn.Dropout(dropout_rate * 0.5),
                nn.Linear(hidden_dims[-1] // 2, 1)
            )
            for _ in range(num_diseases)
        ])
        
        # Global disease classifier
        self.global_classifier = nn.Sequential(
            nn.Linear(hidden_dims[-1], hidden_dims[-1] // 2),
            nn.GELU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_dims[-1] // 2, num_diseases)
        )
        
        # Multi-task heads
        
        # Confidence estimation (how sure the model is)
        self.confidence_estimator = nn.Sequential(
            nn.Linear(hidden_dims[-1], 64),
            nn.GELU(),
            nn.Dropout(dropout_rate * 0.5),
            nn.Linear(64, 32),
            nn.GELU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )
        
        # Severity prediction (mild, moderate, severe)
        self.severity_predictor = nn.Sequential(
            nn.Linear(hidden_dims[-1], 64),
            nn.GELU(),
            nn.Dropout(dropout_rate * 0.5),
            nn.Linear(64, 3)
        )
        
        # Urgency prediction (normal, low, medium, high, emergency)
        self.urgency_predictor = nn.Sequential(
            nn.Linear(hidden_dims[-1], 64),
            nn.GELU(),
            nn.Dropout(dropout_rate * 0.5),
            nn.Linear(64, 5)
        )
        
        # Symptom clustering (group related symptoms)
        self.symptom_clusterer = nn.Sequential(
            nn.Linear(num_symptoms, 128),
            nn.GELU(),
            nn.Linear(128, 64),
            nn.GELU(),
            nn.Linear(64, 10)  # 10 symptom clusters
        )
        
        # Initialize weights
        self._initialize_weights()
    
    def _initialize_weights(self):
        """Initialize network weights using best practices"""
        for module in self.modules():
            if isinstance(module, nn.Linear):
                # He initialization for GELU activation
                nn.init.kaiming_normal_(module.weight, mode='fan_in', nonlinearity='relu')
                if module.bias is not None:
                    nn.init.constant_(module.bias, 0)
            elif isinstance(module, nn.BatchNorm1d):
                nn.init.constant_(module.weight, 1)
                nn.init.constant_(module.bias, 0)
    
    def forward(self, symptom_vector, return_features=False):
        batch_size = symptom_vector.size(0)
        
        # Apply learned symptom importance weights
        weighted_symptoms = symptom_vector * torch.sigmoid(self.symptom_weights)
        
        # Input embedding
        x = self.input_embedding(weighted_symptoms)
        
        # Store intermediate features for analysis
        features = {'input': x.clone()}
        
        # Apply attention to understand symptom relationships
        attention_weights = None
        if self.use_attention:
            x, attention_weights = self.symptom_attention(x)
            features['attention'] = x.clone()
        
        # Pass through feature extraction layers
        for i, layer in enumerate(self.feature_layers):
            x = layer(x)
            features[f'layer_{i}'] = x.clone()
        
        # Final feature representation
        final_features = x
        
        # Disease predictions
        
        # 1. Global classifier (main prediction)
        global_logits = self.global_classifier(final_features)
        
        # 2. Disease-specific classifiers (ensemble approach)
        disease_specific_scores = []
        for disease_layer in self.disease_specific_layers:
            score = disease_layer(final_features)
            disease_specific_scores.append(score)
        
        disease_specific_logits = torch.cat(disease_specific_scores, dim=1)
        
        # Combine global and disease-specific predictions
        alpha = 0.7  # Weight for global vs specific predictions
        combined_logits = alpha * global_logits + (1 - alpha) * disease_specific_logits
        
        # Multi-task predictions
        confidence = self.confidence_estimator(final_features)
        severity_logits = self.severity_predictor(final_features)
        urgency_logits = self.urgency_predictor(final_features)
        
        # Symptom clustering
        symptom_clusters = self.symptom_clusterer(weighted_symptoms)
        
        # Prepare output
        output = {
            'disease_logits': combined_logits,
            'global_logits': global_logits,
            'disease_specific_logits': disease_specific_logits,
            'confidence': confidence,
            'severity_logits': severity_logits,
            'urgency_logits': urgency_logits,
            'symptom_clusters': symptom_clusters,
            'symptom_weights': torch.sigmoid(self.symptom_weights),
            'attention_weights': attention_weights
        }
        
        if return_features:
            output['features'] = features
            output['final_features'] = final_features
        
        return output
    
    def get_symptom_importance(self):
        """Get learned symptom importance weights"""
        return torch.sigmoid(self.symptom_weights).detach().cpu().numpy()
    
    def interpret_prediction(self, symptom_vector, symptom_names=None):
        """Provide interpretation of the model's prediction"""
        self.eval()
        with torch.no_grad():
            output = self.forward(symptom_vector, return_features=True)
            
            # Get predictions
            disease_probs = F.softmax(output['disease_logits'], dim=1)
            confidence = output['confidence']
            
            # Get symptom contributions
            symptom_weights = output['symptom_weights']
            symptom_contributions = symptom_vector * symptom_weights
            
            interpretation = {
                'disease_probabilities': disease_probs.cpu().numpy(),
                'confidence': confidence.cpu().numpy(),
                'symptom_contributions': symptom_contributions.cpu().numpy(),
                'attention_weights': output['attention_weights'].cpu().numpy() if output['attention_weights'] is not None else None,
                'top_contributing_symptoms': self._get_top_symptoms(symptom_contributions, symptom_names)
            }
            
            return interpretation
    
    def _get_top_symptoms(self, symptom_contributions, symptom_names=None, top_k=5):
        """Get top contributing symptoms for interpretation"""
        if symptom_names is None:
            symptom_names = [f"Symptom_{i}" for i in range(len(symptom_contributions[0]))]
        
        top_symptoms = []
        for batch_idx in range(symptom_contributions.size(0)):
            contributions = symptom_contributions[batch_idx]
            top_indices = torch.argsort(contributions, descending=True)[:top_k]
            
            batch_top_symptoms = []
            for idx in top_indices:
                if contributions[idx] > 0:  # Only include active symptoms
                    batch_top_symptoms.append({
                        'name': symptom_names[idx],
                        'contribution': contributions[idx].item(),
                        'index': idx.item()
                    })
            
            top_symptoms.append(batch_top_symptoms)
        
        return top_symptoms

# Advanced Loss Functions for better training

class FocalLoss(nn.Module):
    """Focal Loss for handling class imbalance"""
    
    def __init__(self, alpha=1.0, gamma=2.0, reduction='mean'):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction
    
    def forward(self, inputs, targets):
        ce_loss = F.cross_entropy(inputs, targets, reduction='none')
        pt = torch.exp(-ce_loss)
        focal_loss = self.alpha * (1 - pt) ** self.gamma * ce_loss
        
        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        else:
            return focal_loss

class MultiTaskLoss(nn.Module):
    """Multi-task loss combining disease prediction with auxiliary tasks"""
    
    def __init__(self, task_weights=None):
        super(MultiTaskLoss, self).__init__()
        
        if task_weights is None:
            task_weights = {
                'disease': 1.0,
                'confidence': 0.3,
                'severity': 0.2,
                'urgency': 0.2
            }
        
        self.task_weights = task_weights
        self.focal_loss = FocalLoss(alpha=1.0, gamma=2.0)
        
    def forward(self, outputs, targets):
        # Main disease prediction loss
        disease_loss = self.focal_loss(outputs['disease_logits'], targets['disease'])
        
        total_loss = self.task_weights['disease'] * disease_loss
        loss_dict = {'disease_loss': disease_loss}
        
        # Confidence loss (if available)
        if 'confidence' in targets and 'confidence' in outputs:
            confidence_loss = F.mse_loss(outputs['confidence'], targets['confidence'])
            total_loss += self.task_weights['confidence'] * confidence_loss
            loss_dict['confidence_loss'] = confidence_loss
        
        # Severity loss (if available)
        if 'severity' in targets and 'severity_logits' in outputs:
            severity_loss = F.cross_entropy(outputs['severity_logits'], targets['severity'])
            total_loss += self.task_weights['severity'] * severity_loss
            loss_dict['severity_loss'] = severity_loss
        
        # Urgency loss (if available)
        if 'urgency' in targets and 'urgency_logits' in outputs:
            urgency_loss = F.cross_entropy(outputs['urgency_logits'], targets['urgency'])
            total_loss += self.task_weights['urgency'] * urgency_loss
            loss_dict['urgency_loss'] = urgency_loss
        
        loss_dict['total_loss'] = total_loss
        return total_loss, loss_dict

# Example usage and testing
def test_improved_model():
    """Test the improved model"""
    
    # Model parameters
    num_symptoms = 15
    num_diseases = 10
    batch_size = 8
    
    # Create model
    model = ImprovedDiseasePredictionNetwork(
        num_symptoms=num_symptoms,
        num_diseases=num_diseases,
        hidden_dims=[512, 256, 128],
        use_attention=True,
        use_residual=True,
        dropout_rate=0.3
    )
    
    # Create sample data
    symptom_vector = torch.randn(batch_size, num_symptoms)
    symptom_vector = torch.clamp(symptom_vector, min=0, max=3)  # Simulate symptom severity
    
    # Forward pass
    print("Testing improved model...")
    output = model(symptom_vector, return_features=True)
    
    print(f"Input shape: {symptom_vector.shape}")
    print(f"Disease logits shape: {output['disease_logits'].shape}")
    print(f"Confidence shape: {output['confidence'].shape}")
    print(f"Severity logits shape: {output['severity_logits'].shape}")
    print(f"Urgency logits shape: {output['urgency_logits'].shape}")
    print(f"Symptom clusters shape: {output['symptom_clusters'].shape}")
    
    # Test interpretation
    interpretation = model.interpret_prediction(symptom_vector[:1])
    print(f"Disease probabilities: {interpretation['disease_probabilities'][0][:5]}")
    print(f"Confidence: {interpretation['confidence'][0]}")
    print(f"Top symptoms: {interpretation['top_contributing_symptoms'][0][:3]}")
    
    # Test multi-task loss
    targets = {
        'disease': torch.randint(0, num_diseases, (batch_size,)),
        'severity': torch.randint(0, 3, (batch_size,)),
        'urgency': torch.randint(0, 5, (batch_size,))
    }
    
    criterion = MultiTaskLoss()
    loss, loss_dict = criterion(output, targets)
    
    print(f"Total loss: {loss.item():.4f}")
    for key, value in loss_dict.items():
        if key != 'total_loss':
            print(f"{key}: {value.item():.4f}")
    
    print("Model test completed successfully!")

if __name__ == "__main__":
    test_improved_model()