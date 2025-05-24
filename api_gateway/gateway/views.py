import requests
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

def proxy_request(service_name, path, method='GET', data=None, user=None):
    """Proxy request to microservice"""
    service_url = settings.MICROSERVICES.get(service_name)
    if not service_url:
        return {'error': 'Service not found'}, 404
    
    url = f"{service_url}/{path}"
    headers = {}
    
    if user and hasattr(user, 'auth_token'):
        headers['Authorization'] = f'Token {user.auth_token.key}'
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, params=data)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=data)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        
        return response.json(), response.status_code
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}, 500

# User Service Endpoints
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data, status_code = proxy_request('user_service', 'api/v1/users/register/', 'POST', request.data)
    return Response(data, status=status_code)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    data, status_code = proxy_request('user_service', 'api/v1/users/login/', 'POST', request.data)
    return Response(data, status=status_code)

# Patient Service Endpoints
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def patients(request):
    if request.method == 'GET':
        data, status_code = proxy_request('patient_service', 'api/v1/patients/', 'GET', request.GET, request.user)
    else:
        data, status_code = proxy_request('patient_service', 'api/v1/patients/', 'POST', request.data, request.user)
    return Response(data, status=status_code)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def patient_detail(request, patient_id):
    path = f'api/v1/patients/{patient_id}/'
    data, status_code = proxy_request('patient_service', path, request.method, request.data, request.user)
    return Response(data, status=status_code)

# Doctor Service Endpoints
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def doctors(request):
    if request.method == 'GET':
        data, status_code = proxy_request('doctor_service', 'api/v1/doctors/', 'GET', request.GET, request.user)
    else:
        data, status_code = proxy_request('doctor_service', 'api/v1/doctors/', 'POST', request.data, request.user)
    return Response(data, status=status_code)

# Appointment Service Endpoints
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def appointments(request):
    if request.method == 'GET':
        data, status_code = proxy_request('appointment_service', 'api/v1/appointments/', 'GET', request.GET, request.user)
    else:
        data, status_code = proxy_request('appointment_service', 'api/v1/appointments/', 'POST', request.data, request.user)
    return Response(data, status=status_code)

# Chatbot Service Endpoints
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_chat_session(request):
    data, status_code = proxy_request('chatbot_service', 'api/v1/chatbot/sessions/', 'POST', request.data, request.user)
    return Response(data, status=status_code)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_chat_message(request):
    data, status_code = proxy_request('chatbot_service', 'api/v1/chatbot/message/', 'POST', request.data, request.user)
    return Response(data, status=status_code)

# api_gateway/urls.py
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # User Service
    path('api/v1/users/register/', views.register_user, name='register'),
    path('api/v1/users/login/', views.login_user, name='login'),
    
    # Patient Service
    path('api/v1/patients/', views.patients, name='patients'),
    path('api/v1/patients/<int:patient_id>/', views.patient_detail, name='patient-detail'),
    
    # Doctor Service
    path('api/v1/doctors/', views.doctors, name='doctors'),
    
    # Appointment Service
    path('api/v1/appointments/', views.appointments, name='appointments'),
    
    # Chatbot Service
    path('api/v1/chatbot/sessions/', views.create_chat_session, name='create-chat'),
    path('api/v1/chatbot/message/', views.send_chat_message, name='send-message'),
]