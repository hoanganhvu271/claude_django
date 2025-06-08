from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

# Initialize ML Engine
ml_engine = MLEngine()

@api_view(['POST'])
@permission_classes([AllowAny])
def predict_disease(request):
    """Main API endpoint for disease prediction"""
    symptoms_text = request.data.get('symptoms', '').strip()
    
    if not symptoms_text:
        return Response({'error': 'Symptoms text is required'}, status=400)
    
    try:
        # Get predictions
        predictions = ml_engine.predict_disease(symptoms_text)
        
        # Format response
        if predictions and predictions[0].get('confidence', 0) > 0.1:
            # Build response message
            response_text = "🔍 **Kết quả dự đoán bệnh:**\n\n"
            
            for i, pred in enumerate(predictions[:3], 1):
                confidence_percent = int(pred['confidence'] * 100)
                response_text += f"{i}. **{pred['disease']}** - {confidence_percent}% tin cậy\n"
            
            # Add extracted symptoms
            if predictions[0].get('extracted_symptoms'):
                response_text += f"\n**Triệu chứng đã nhận diện:** {', '.join(predictions[0]['extracted_symptoms'])}\n"
            
            # Add recommendations for top prediction
            top_disease = predictions[0]['disease']
            try:
                from .models import Disease
                disease_obj = Disease.objects.get(name=top_disease)
                response_text += f"\n**💡 Khuyến nghị:** {disease_obj.recommendations}\n"
                
                if disease_obj.severity_level == 'emergency':
                    response_text += "\n🚨 **CẢNH BÁO:** Cần chăm sóc y tế khẩn cấp!"
                    
            except Disease.DoesNotExist:
                pass
            
            urgency_level = 'emergency' if any(p.get('confidence', 0) > 0.8 and 'tim' in p.get('disease', '').lower() for p in predictions) else 'normal'
            
        else:
            response_text = "Không thể xác định bệnh cụ thể từ triệu chứng đã mô tả.\nKhuyến nghị tham khảo ý kiến bác sĩ chuyên khoa."
            urgency_level = 'normal'
        
        response_text += "\n\n⚠️ **Lưu ý:** Đây chỉ là dự đoán tham khảo. Hãy luôn tham khảo ý kiến bác sĩ."
        
        return Response({
            'message': response_text,
            'predictions': predictions,
            'extracted_symptoms': predictions[0].get('extracted_symptoms', []) if predictions else [],
            'urgency_level': urgency_level,
            'confidence_level': 'high' if predictions and predictions[0].get('confidence', 0) > 0.7 else 'medium' if predictions and predictions[0].get('confidence', 0) > 0.4 else 'low'
        })
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return Response({'error': 'Prediction failed', 'details': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def setup_system(request):
    """Setup the complete ML system"""
    try:
        # Create medical data
        results = MedicalDataLoader.create_medical_data(ml_engine)
        
        return Response({
            'message': 'System setup completed',
            'created_data': results,
            'next_step': 'Train the model using /train-model/ endpoint'
        })
        
    except Exception as e:
        logger.error(f"Setup error: {e}")
        return Response({'error': f'Setup failed: {str(e)}'}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def train_model(request):
    """Train the ML model"""
    try:
        # Check data availability
        from .models import Disease, Symptom, DiseaseSymptom
        
        diseases_count = Disease.objects.count()
        symptoms_count = Symptom.objects.count()
        relations_count = DiseaseSymptom.objects.count()
        
        if diseases_count < 3 or symptoms_count < 5 or relations_count < 10:
            return Response({
                'error': 'Insufficient training data',
                'current_data': {
                    'diseases': diseases_count,
                    'symptoms': symptoms_count,
                    'relations': relations_count
                },
                'minimum_required': {
                    'diseases': 3,
                    'symptoms': 5,
                    'relations': 10
                }
            }, status=400)
        
        # Train model
        success = ml_engine.train_model()
        
        if success:
            return Response({
                'message': 'Model training completed successfully',
                'model_info': ml_engine.get_model_info()
            })
        else:
            return Response({'error': 'Model training failed'}, status=500)
            
    except Exception as e:
        logger.error(f"Training error: {e}")
        return Response({'error': f'Training failed: {str(e)}'}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_model_status(request):
    """Get current model status and system information"""
    try:
        from .models import Disease, Symptom, DiseaseSymptom, KnowledgeBase
        
        model_info = ml_engine.get_model_info()
        
        system_stats = {
            'diseases_count': Disease.objects.count(),
            'symptoms_count': Symptom.objects.count(),
            'relations_count': DiseaseSymptom.objects.count(),
            'knowledge_count': KnowledgeBase.objects.count()
        }
        
        return Response({
            'model_info': model_info,
            'system_stats': system_stats,
            'ready_for_prediction': model_info['model_loaded'] and system_stats['diseases_count'] > 0
        })
        
    except Exception as e:
        logger.error(f"Status check error: {e}")
        return Response({'error': f'Status check failed: {str(e)}'}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def extract_symptoms_only(request):
    """Extract symptoms from text without prediction"""
    text = request.data.get('text', '').strip()
    
    if not text:
        return Response({'error': 'Text is required'}, status=400)
    
    try:
        extracted = ml_engine.symptom_extractor.extract_symptoms(text)
        
        return Response({
            'extracted_symptoms': extracted,
            'total_found': len(extracted)
        })
        
    except Exception as e:
        logger.error(f"Symptom extraction error: {e}")
        return Response({'error': f'Extraction failed: {str(e)}'}, status=500)

# urls.py
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
]