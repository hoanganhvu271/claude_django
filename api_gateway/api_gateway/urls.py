from django.urls import path
from django.http import JsonResponse
from gateway import views

def api_status(request):
    return JsonResponse({
        'status': 'OK',
        'message': 'Healthcare Management API Gateway',
        'version': '1.0.0'
    })

urlpatterns = [
    # API Status
    path('', api_status, name='api-status'),
    path('api/v1/', api_status, name='api-status-v1'),
    
    # Authentication endpoints
    path('api/v1/users/register/', views.register_user, name='register'),
    path('api/v1/users/login/', views.login_user, name='login'),
    
    # Patient endpoints
    path('api/v1/patients/', views.patients, name='patients'),
    path('api/v1/patients/<int:patient_id>/', views.patient_detail, name='patient-detail'),
    
    # Doctor endpoints
    path('api/v1/doctors/', views.doctors, name='doctors'),
    path('api/v1/doctors/<int:doctor_id>/', views.doctor_detail, name='doctor-detail'),
    
    # Appointment endpoints
    path('api/v1/appointments/', views.appointments, name='appointments'),
    path('api/v1/appointments/<int:appointment_id>/', views.appointment_detail, name='appointment-detail'),
    
    # Health Record endpoints
    path('api/v1/health-records/', views.health_records, name='health-records'),
    path('api/v1/health-records/<int:record_id>/', views.health_record_detail, name='health-record-detail'),
    path('api/v1/patients/<int:patient_id>/health-records/', views.patient_health_records, name='patient-health-records'),
    path('api/v1/patients/<int:patient_id>/allergies/', views.patient_allergies, name='patient-allergies'),
    
    # Chatbot endpoints
    path('api/v1/chatbot/sessions/', views.create_chat_session, name='create-chat'),
    path('api/v1/chatbot/message/', views.send_chat_message, name='send-message'),

    
]