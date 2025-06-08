from django.urls import path
from . import views

urlpatterns = [
    # Core prediction
    path('api/predict/', views.predict_disease, name='predict-disease'),
    
    # System management
    path('api/setup/', views.setup_system, name='setup-system'),
    path('api/train/', views.train_model, name='train-model'),
    path('api/status/', views.get_model_status, name='model-status'),
    
    # Utilities
    path('api/extract-symptoms/', views.extract_symptoms_only, name='extract-symptoms'),
    
    # Health check
    path('health/', views.health_check, name='health-check'),
]