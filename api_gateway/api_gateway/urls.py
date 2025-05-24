from django.urls import path
from gateway import views

urlpatterns = [
    # Authentication endpoints
    path('api/v1/users/register/', views.register_user, name='register'),
    path('api/v1/users/login/', views.login_user, name='login'),
    
    # Patient endpoints
    path('api/v1/patients/', views.patients, name='patients'),
    path('api/v1/patients/<int:patient_id>/', views.patient_detail, name='patient-detail'),
    
    # Doctor endpoints
    path('api/v1/doctors/', views.doctors, name='doctors'),
    
    # Appointment endpoints
    path('api/v1/appointments/', views.appointments, name='appointments'),
    
    # Chatbot endpoints
    path('api/v1/chatbot/sessions/', views.create_chat_session, name='create-chat'),
    path('api/v1/chatbot/message/', views.send_chat_message, name='send-message'),
]