import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key-here-change-in-production'
DEBUG = True
ALLOWED_HOSTS = ['*']

# Apps required for authentication
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',  # Thêm sessions
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'gateway',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Thêm session middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api_gateway.urls'

# Use SQLite for simplicity
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        # Loại bỏ BrowsableAPIRenderer để tránh cần template
    ],
}

# Service URLs - matching run_all.bat ports
MICROSERVICES = {
    'user_service': 'http://localhost:8001',
    'patient_service': 'http://localhost:8002',
    'doctor_service': 'http://localhost:8003',
    'nurse_service': 'http://localhost:8004',
    'appointment_service': 'http://localhost:8005',
    'health_record_service': 'http://localhost:8006',
    'medication_service': 'http://localhost:8007',
    'laboratory_service': 'http://localhost:8008',
    'pharmacy_service': 'http://localhost:8009',
    'invoice_service': 'http://localhost:8010',
    'payment_service': 'http://localhost:8011',
    'notification_service': 'http://localhost:8012',
    'insurance_service': 'http://localhost:8013',
    'chatbot_service': 'http://localhost:8014',
}

CORS_ALLOW_ALL_ORIGINS = True

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Service Port
SERVICE_PORT = 8000