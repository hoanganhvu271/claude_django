import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import List, Tuple, Dict

class DiseasePredictionNetwork(nn.Module):
    """Neural Network for Disease Prediction from Symptoms"""
    
    def __init__(self, num_symptoms: int, num_diseases: int, hidden_dims: List[int] = [512, 256, 128]):
        super(DiseasePredictionNetwork, self).__init__()
        
        self.num_symptoms = num_symptoms
        self.num_diseases = num_diseases
        
        # Symptom attention layer
        self.symptom_attention = nn.Sequential(
            nn.Linear(num_symptoms, 256),
            nn.Tanh(),
            nn.Linear(256, num_symptoms),
            nn.Softmax(dim=1)
        )
        
        # Main prediction network
        layers = []
        prev_dim = num_symptoms
        
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.BatchNorm1d(hidden_dim),
                nn.ReLU(),
                nn.Dropout(0.3)
            ])
            prev_dim = hidden_dim
        
        # Output layer
        layers.append(nn.Linear(prev_dim, num_diseases))
        
        self.prediction_network = nn.Sequential(*layers)
        
        # Disease confidence estimation
        self.confidence_estimator = nn.Sequential(
            nn.Linear(prev_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
    
    def forward(self, symptom_vector):
        # Apply attention to symptoms
        attention_weights = self.symptom_attention(symptom_vector)
        attended_symptoms = symptom_vector * attention_weights
        
        # Get features before final layer
        features = attended_symptoms
        for layer in self.prediction_network[:-1]:
            features = layer(features)
        
        # Disease predictions
        disease_logits = self.prediction_network[-1](features)
        
        # Confidence estimation
        confidence = self.confidence_estimator(features)
        
        return disease_logits, attention_weights, confidence