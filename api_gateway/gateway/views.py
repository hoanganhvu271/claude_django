import requests
import json
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

def proxy_request(service_name, path, method='GET', data=None, user=None):
    """Proxy request to microservice with better error handling"""
    service_url = settings.MICROSERVICES.get(service_name)
    if not service_url:
        return {'error': f'Service {service_name} not found'}, 404
    
    url = f"{service_url}/{path}"
    headers = {'Content-Type': 'application/json'}
    
    if user and hasattr(user, 'auth_token'):
        headers['Authorization'] = f'Token {user.auth_token.key}'
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, params=data, timeout=10)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data, timeout=10)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=data, timeout=10)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=10)
        
        # Check if response is successful
        if response.status_code in [200, 201]:
            try:
                return response.json(), response.status_code
            except json.JSONDecodeError:
                return {'error': 'Invalid JSON response from service', 'raw_response': response.text}, 500
        else:
            try:
                error_data = response.json()
                return error_data, response.status_code
            except json.JSONDecodeError:
                return {'error': f'Service error: {response.status_code}', 'raw_response': response.text}, response.status_code
                
    except requests.exceptions.ConnectionError:
        return {'error': f'Cannot connect to {service_name} service. Is it running on {service_url}?'}, 503
    except requests.exceptions.Timeout:
        return {'error': f'Timeout connecting to {service_name} service'}, 504
    except requests.exceptions.RequestException as e:
        return {'error': f'Request failed: {str(e)}'}, 500

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
@permission_classes([AllowAny])
def patients(request):
    if request.method == 'GET':
        data, status_code = proxy_request('patient_service', 'api/v1/patients/', 'GET', request.GET, request.user)
    else:
        data, status_code = proxy_request('patient_service', 'api/v1/patients/', 'POST', request.data, request.user)
    return Response(data, status=status_code)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def patient_detail(request, patient_id):
    path = f'api/v1/patients/{patient_id}/'
    data, status_code = proxy_request('patient_service', path, request.method, request.data, request.user)
    return Response(data, status=status_code)

# Doctor Service Endpoints
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # Allow anyone to view doctors list
def doctors(request):
    if request.method == 'GET':
        data, status_code = proxy_request('doctor_service', 'api/v1/doctors/', 'GET', request.GET, request.user)
    else:
        data, status_code = proxy_request('doctor_service', 'api/v1/doctors/', 'POST', request.data, request.user)
    return Response(data, status=status_code)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def doctor_detail(request, doctor_id):
    path = f'api/v1/doctors/{doctor_id}/'
    data, status_code = proxy_request('doctor_service', path, request.method, request.data, request.user)
    return Response(data, status=status_code)

# Appointment Service Endpoints
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def appointments(request):
    if request.method == 'GET':
        data, status_code = proxy_request('appointment_service', 'api/v1/appointments/', 'GET', request.GET, request.user)
    else:
        data, status_code = proxy_request('appointment_service', 'api/v1/appointments/', 'POST', request.data, request.user)
    return Response(data, status=status_code)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def appointment_detail(request, appointment_id):
    path = f'api/v1/appointments/{appointment_id}/'
    data, status_code = proxy_request('appointment_service', path, request.method, request.data, request.user)
    return Response(data, status=status_code)

# Chatbot Service Endpoints
@api_view(['POST'])
@permission_classes([AllowAny])
def create_chat_session(request):
    data, status_code = proxy_request('chatbot_service', 'api/v1/chatbot/sessions/', 'POST', request.data, request.user)
    return Response(data, status=status_code)

@api_view(['POST'])
@permission_classes([AllowAny])
def send_chat_message(request):
    data, status_code = proxy_request('chatbot_service', 'api/v1/chatbot/message/', 'POST', request.data, request.user)
    return Response(data, status=status_code)