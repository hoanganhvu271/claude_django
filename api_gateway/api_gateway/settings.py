import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key-here'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api_gateway.urls'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Service URLs
MICROSERVICES = {
    'user_service': 'http://localhost:8001',
    'patient_service': 'http://localhost:8002',
    'doctor_service': 'http://localhost:8003',
    'appointment_service': 'http://localhost:8004',
    'health_record_service': 'http://localhost:8005',
    'medication_service': 'http://localhost:8006',
    'laboratory_service': 'http://localhost:8007',
    'pharmacy_service': 'http://localhost:8008',
    'invoice_service': 'http://localhost:8009',
    'payment_service': 'http://localhost:8010',
    'notification_service': 'http://localhost:8011',
    'insurance_service': 'http://localhost:8012',
    'chatbot_service': 'http://localhost:8013',
    'nurse_service': 'http://localhost:8014',
}

CORS_ALLOW_ALL_ORIGINS = True