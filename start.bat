@echo off
echo ================================================
echo Healthcare Microservices Setup Script
echo ================================================
echo.

REM Create main project directory
echo Creating main project directory...
mkdir healthcare_microservices
cd healthcare_microservices

REM Create requirements.txt
echo Creating requirements.txt...
(
echo Django==4.2.7
echo djangorestframework==3.14.0
echo django-cors-headers==4.3.1
echo psycopg2-binary==2.9.8
echo redis==5.0.1
echo celery==5.3.4
echo requests==2.31.0
echo python-decouple==3.8
echo gunicorn==21.2.0
echo django-filter==23.3
echo Pillow==10.0.1
) > requirements.txt

REM Install requirements
echo Installing Python requirements...
pip install -r requirements.txt

REM Array of services
set services=user_service patient_service doctor_service nurse_service appointment_service health_record_service medication_service laboratory_service pharmacy_service invoice_service payment_service notification_service insurance_service chatbot_service api_gateway

echo.
echo Creating Django services...
echo.

REM Create each service
for %%s in (%services%) do (
    echo Creating %%s...
    django-admin startproject %%s
    cd %%s
    
    REM Create apps for each service
    if "%%s"=="api_gateway" (
        python manage.py startapp gateway
    ) else (
        python manage.py startapp %%s_app
    )
    
    REM Create models.py for each service
    call :create_models %%s
    
    REM Create serializers.py for each service
    call :create_serializers %%s
    
    REM Create views.py for each service
    call :create_views %%s
    
    REM Create urls.py for each service
    call :create_urls %%s
    
    REM Update settings.py
    call :update_settings %%s
    
    REM Create Dockerfile
    call :create_dockerfile %%s
    
    cd ..
    echo %%s created successfully!
    echo.
)

REM Create docker-compose.yml
call :create_docker_compose

REM Create run_all.bat script
call :create_run_script

echo ================================================
echo Setup completed successfully!
echo ================================================
echo.
echo Next steps:
echo 1. Configure databases for each service
echo 2. Run migrations: python manage.py migrate
echo 3. Create superuser: python manage.py createsuperuser
echo 4. Start services using run_all.bat
echo.
pause
goto :eof

REM Function to create models.py
:create_models
if "%1"=="user_service" (
    (
    echo from django.contrib.auth.models import AbstractUser
    echo from django.db import models
    echo.
    echo class User^(AbstractUser^):
    echo     ROLE_CHOICES = [
    echo         ^('patient', 'Patient'^),
    echo         ^('doctor', 'Doctor'^),
    echo         ^('nurse', 'Nurse'^),
    echo         ^('admin', 'Administrator'^),
    echo         ^('pharmacist', 'Pharmacist'^),
    echo         ^('lab_tech', 'Laboratory Technician'^),
    echo         ^('insurance', 'Insurance Provider'^),
    echo     ]
    echo     email = models.EmailField^(unique=True^)
    echo     phone = models.CharField^(max_length=15, blank=True^)
    echo     role = models.CharField^(max_length=20, choices=ROLE_CHOICES^)
    echo     is_verified = models.BooleanField^(default=False^)
    echo     created_at = models.DateTimeField^(auto_now_add=True^)
    echo     updated_at = models.DateTimeField^(auto_now=True^)
    ) > user_service_app\models.py
)

if "%1"=="patient_service" (
    (
    echo from django.db import models
    echo.
    echo class Patient^(models.Model^):
    echo     user_id = models.IntegerField^(unique=True^)
    echo     first_name = models.CharField^(max_length=100^)
    echo     last_name = models.CharField^(max_length=100^)
    echo     date_of_birth = models.DateField^(^)
    echo     gender = models.CharField^(max_length=10, choices=[^('M', 'Male'^), ^('F', 'Female'^)]^)
    echo     blood_type = models.CharField^(max_length=5, blank=True^)
    echo     address = models.TextField^(^)
    echo     emergency_contact_name = models.CharField^(max_length=100^)
    echo     emergency_contact_phone = models.CharField^(max_length=15^)
    echo     insurance_number = models.CharField^(max_length=50, blank=True^)
    echo     allergies = models.TextField^(blank=True^)
    echo     created_at = models.DateTimeField^(auto_now_add=True^)
    echo     updated_at = models.DateTimeField^(auto_now=True^)
    echo.
    echo     def __str__^(self^):
    echo         return f"{self.first_name} {self.last_name}"
    ) > patient_service_app\models.py
)

if "%1"=="doctor_service" (
    (
    echo from django.db import models
    echo.
    echo class Doctor^(models.Model^):
    echo     user_id = models.IntegerField^(unique=True^)
    echo     first_name = models.CharField^(max_length=100^)
    echo     last_name = models.CharField^(max_length=100^)
    echo     specialization = models.CharField^(max_length=100^)
    echo     license_number = models.CharField^(max_length=50, unique=True^)
    echo     qualification = models.TextField^(^)
    echo     experience_years = models.IntegerField^(^)
    echo     consultation_fee = models.DecimalField^(max_digits=10, decimal_places=2^)
    echo     is_available = models.BooleanField^(default=True^)
    echo     created_at = models.DateTimeField^(auto_now_add=True^)
    echo.
    echo     def __str__^(self^):
    echo         return f"Dr. {self.first_name} {self.last_name}"
    echo.
    echo class DoctorAvailability^(models.Model^):
    echo     doctor = models.ForeignKey^(Doctor, on_delete=models.CASCADE^)
    echo     day_of_week = models.IntegerField^(^)
    echo     start_time = models.TimeField^(^)
    echo     end_time = models.TimeField^(^)
    echo     is_available = models.BooleanField^(default=True^)
    ) > doctor_service_app\models.py
)

if "%1"=="appointment_service" (
    (
    echo from django.db import models
    echo.
    echo class Appointment^(models.Model^):
    echo     STATUS_CHOICES = [
    echo         ^('scheduled', 'Scheduled'^),
    echo         ^('confirmed', 'Confirmed'^),
    echo         ^('completed', 'Completed'^),
    echo         ^('cancelled', 'Cancelled'^),
    echo         ^('no_show', 'No Show'^),
    echo     ]
    echo     patient_id = models.IntegerField^(^)
    echo     doctor_id = models.IntegerField^(^)
    echo     appointment_date = models.DateField^(^)
    echo     appointment_time = models.TimeField^(^)
    echo     duration_minutes = models.IntegerField^(default=30^)
    echo     status = models.CharField^(max_length=20, choices=STATUS_CHOICES, default='scheduled'^)
    echo     reason = models.TextField^(^)
    echo     notes = models.TextField^(blank=True^)
    echo     created_at = models.DateTimeField^(auto_now_add=True^)
    echo     updated_at = models.DateTimeField^(auto_now=True^)
    echo.
    echo     class Meta:
    echo         unique_together = ['doctor_id', 'appointment_date', 'appointment_time']
    ) > appointment_service_app\models.py
)

REM Add similar model creation for other services...
goto :eof

REM Function to create serializers.py
:create_serializers
if "%1"=="user_service" (
    (
    echo from rest_framework import serializers
    echo from django.contrib.auth import authenticate
    echo from .models import User
    echo.
    echo class UserRegistrationSerializer^(serializers.ModelSerializer^):
    echo     password = serializers.CharField^(write_only=True^)
    echo     password_confirm = serializers.CharField^(write_only=True^)
    echo.
    echo     class Meta:
    echo         model = User
    echo         fields = ['username', 'email', 'password', 'password_confirm', 'phone', 'role']
    echo.
    echo     def validate^(self, data^):
    echo         if data['password'] != data['password_confirm']:
    echo             raise serializers.ValidationError^("Passwords don't match"^)
    echo         return data
    echo.
    echo     def create^(self, validated_data^):
    echo         validated_data.pop^('password_confirm'^)
    echo         password = validated_data.pop^('password'^)
    echo         user = User^(**validated_data^)
    echo         user.set_password^(password^)
    echo         user.save^(^)
    echo         return user
    echo.
    echo class UserSerializer^(serializers.ModelSerializer^):
    echo     class Meta:
    echo         model = User
    echo         fields = ['id', 'username', 'email', 'phone', 'role', 'is_verified', 'created_at']
    ) > user_service_app\serializers.py
)

REM Add similar serializer creation for other services...
goto :eof

REM Function to create views.py
:create_views
if "%1"=="user_service" (
    (
    echo from rest_framework import status, generics
    echo from rest_framework.decorators import api_view
    echo from rest_framework.response import Response
    echo from rest_framework.authtoken.models import Token
    echo from .models import User
    echo from .serializers import UserRegistrationSerializer, UserSerializer
    echo.
    echo @api_view^(['POST']^)
    echo def register_user^(request^):
    echo     serializer = UserRegistrationSerializer^(data=request.data^)
    echo     if serializer.is_valid^(^):
    echo         user = serializer.save^(^)
    echo         token, created = Token.objects.get_or_create^(user=user^)
    echo         return Response^({
    echo             'user': UserSerializer^(user^).data,
    echo             'token': token.key
    echo         }, status=status.HTTP_201_CREATED^)
    echo     return Response^(serializer.errors, status=status.HTTP_400_BAD_REQUEST^)
    echo.
    echo class UserDetailView^(generics.RetrieveUpdateAPIView^):
    echo     queryset = User.objects.all^(^)
    echo     serializer_class = UserSerializer
    ) > user_service_app\views.py
)

REM Add similar view creation for other services...
goto :eof

REM Function to create urls.py
:create_urls
if "%1"=="user_service" (
    (
    echo from django.urls import path
    echo from . import views
    echo.
    echo urlpatterns = [
    echo     path^('api/v1/users/register/', views.register_user, name='register'^),
    echo     path^('api/v1/users/^<int:pk^>/', views.UserDetailView.as_view^(^), name='user-detail'^),
    echo ]
    ) > user_service_app\urls.py
)

if "%1"=="api_gateway" (
    (
    echo from django.contrib import admin
    echo from django.urls import path, include
    echo from gateway import views
    echo.
    echo urlpatterns = [
    echo     path^('admin/', admin.site.urls^),
    echo     path^('api/v1/users/register/', views.register_user, name='register'^),
    echo     path^('api/v1/users/login/', views.login_user, name='login'^),
    echo     path^('api/v1/patients/', views.patients, name='patients'^),
    echo     path^('api/v1/doctors/', views.doctors, name='doctors'^),
    echo     path^('api/v1/appointments/', views.appointments, name='appointments'^),
    echo     path^('api/v1/chatbot/', include^('gateway.chatbot_urls'^)^),
    echo ]
    ) > api_gateway\urls.py
)

REM Add URL patterns for other services...
goto :eof

REM Function to update settings.py
:update_settings
set port=8000
if "%1"=="user_service" set port=8001
if "%1"=="patient_service" set port=8002
if "%1"=="doctor_service" set port=8003
if "%1"=="nurse_service" set port=8004
if "%1"=="appointment_service" set port=8005
if "%1"=="health_record_service" set port=8006
if "%1"=="medication_service" set port=8007
if "%1"=="laboratory_service" set port=8008
if "%1"=="pharmacy_service" set port=8009
if "%1"=="invoice_service" set port=8010
if "%1"=="payment_service" set port=8011
if "%1"=="notification_service" set port=8012
if "%1"=="insurance_service" set port=8013
if "%1"=="chatbot_service" set port=8014

(
echo import os
echo from pathlib import Path
echo.
echo BASE_DIR = Path^(__file__^).resolve^(^).parent.parent
echo.
echo SECRET_KEY = 'your-secret-key-here-change-in-production'
echo DEBUG = True
echo ALLOWED_HOSTS = ['*']
echo.
echo INSTALLED_APPS = [
echo     'django.contrib.admin',
echo     'django.contrib.auth',
echo     'django.contrib.contenttypes',
echo     'django.contrib.sessions',
echo     'django.contrib.messages',
echo     'django.contrib.staticfiles',
echo     'rest_framework',
echo     'rest_framework.authtoken',
echo     'corsheaders',
echo     '%1_app',
echo ]
echo.
echo MIDDLEWARE = [
echo     'corsheaders.middleware.CorsMiddleware',
echo     'django.middleware.security.SecurityMiddleware',
echo     'django.contrib.sessions.middleware.SessionMiddleware',
echo     'django.middleware.common.CommonMiddleware',
echo     'django.middleware.csrf.CsrfViewMiddleware',
echo     'django.contrib.auth.middleware.AuthenticationMiddleware',
echo     'django.contrib.messages.middleware.MessageMiddleware',
echo     'django.middleware.clickjacking.XFrameOptionsMiddleware',
echo ]
echo.
echo ROOT_URLCONF = '%1.urls'
echo.
echo TEMPLATES = [
echo     {
echo         'BACKEND': 'django.template.backends.django.DjangoTemplates',
echo         'DIRS': [],
echo         'APP_DIRS': True,
echo         'OPTIONS': {
echo             'context_processors': [
echo                 'django.template.context_processors.debug',
echo                 'django.template.context_processors.request',
echo                 'django.contrib.auth.context_processors.auth',
echo                 'django.contrib.messages.context_processors.messages',
echo             ],
echo         },
echo     },
echo ]
echo.
echo WSGI_APPLICATION = '%1.wsgi.application'
echo.
echo DATABASES = {
echo     'default': {
echo         'ENGINE': 'django.db.backends.sqlite3',
echo         'NAME': BASE_DIR / 'db.sqlite3',
echo     }
echo }
echo.
echo REST_FRAMEWORK = {
echo     'DEFAULT_AUTHENTICATION_CLASSES': [
echo         'rest_framework.authentication.TokenAuthentication',
echo     ],
echo     'DEFAULT_PERMISSION_CLASSES': [
echo         'rest_framework.permissions.IsAuthenticated',
echo     ],
echo }
echo.
echo CORS_ALLOW_ALL_ORIGINS = True
echo.
echo LANGUAGE_CODE = 'en-us'
echo TIME_ZONE = 'UTC'
echo USE_I18N = True
echo USE_TZ = True
echo.
echo STATIC_URL = 'static/'
echo.
echo DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
echo.
echo # Service Port
echo SERVICE_PORT = %port%
) > %1\settings.py

goto :eof

REM Function to create Dockerfile
:create_dockerfile
(
echo FROM python:3.11-slim
echo.
echo WORKDIR /app
echo.
echo COPY requirements.txt .
echo RUN pip install -r requirements.txt
echo.
echo COPY . .
echo.
echo EXPOSE 8000
echo.
echo CMD ["gunicorn", "--bind", "0.0.0.0:8000", "%1.wsgi:application"]
) > Dockerfile

goto :eof

REM Function to create docker-compose.yml
:create_docker_compose
(
echo version: '3.8'
echo.
echo services:
echo   postgres:
echo     image: postgres:13
echo     environment:
echo       POSTGRES_DB: healthcare_db
echo       POSTGRES_USER: postgres
echo       POSTGRES_PASSWORD: postgres
echo     ports:
echo       - "5432:5432"
echo     volumes:
echo       - postgres_data:/var/lib/postgresql/data
echo.
echo   redis:
echo     image: redis:6-alpine
echo     ports:
echo       - "6379:6379"
echo.
echo   api_gateway:
echo     build: ./api_gateway
echo     ports:
echo       - "8000:8000"
echo     depends_on:
echo       - postgres
echo       - redis
echo.
echo   user_service:
echo     build: ./user_service
echo     ports:
echo       - "8001:8000"
echo     depends_on:
echo       - postgres
echo.
echo   patient_service:
echo     build: ./patient_service
echo     ports:
echo       - "8002:8000"
echo     depends_on:
echo       - postgres
echo.
echo   doctor_service:
echo     build: ./doctor_service
echo     ports:
echo       - "8003:8000"
echo     depends_on:
echo       - postgres
echo.
echo   nurse_service:
echo     build: ./nurse_service
echo     ports:
echo       - "8004:8000"
echo     depends_on:
echo       - postgres
echo.
echo   appointment_service:
echo     build: ./appointment_service
echo     ports:
echo       - "8005:8000"
echo     depends_on:
echo       - postgres
echo.
echo   health_record_service:
echo     build: ./health_record_service
echo     ports:
echo       - "8006:8000"
echo     depends_on:
echo       - postgres
echo.
echo   medication_service:
echo     build: ./medication_service
echo     ports:
echo       - "8007:8000"
echo     depends_on:
echo       - postgres
echo.
echo   laboratory_service:
echo     build: ./laboratory_service
echo     ports:
echo       - "8008:8000"
echo     depends_on:
echo       - postgres
echo.
echo   pharmacy_service:
echo     build: ./pharmacy_service
echo     ports:
echo       - "8009:8000"
echo     depends_on:
echo       - postgres
echo.
echo   invoice_service:
echo     build: ./invoice_service
echo     ports:
echo       - "8010:8000"
echo     depends_on:
echo       - postgres
echo.
echo   payment_service:
echo     build: ./payment_service
echo     ports:
echo       - "8011:8000"
echo     depends_on:
echo       - postgres
echo.
echo   notification_service:
echo     build: ./notification_service
echo     ports:
echo       - "8012:8000"
echo     depends_on:
echo       - postgres
echo.
echo   insurance_service:
echo     build: ./insurance_service
echo     ports:
echo       - "8013:8000"
echo     depends_on:
echo       - postgres
echo.
echo   chatbot_service:
echo     build: ./chatbot_service
echo     ports:
echo       - "8014:8000"
echo     depends_on:
echo       - postgres
echo.
echo volumes:
echo   postgres_data:
) > docker-compose.yml

goto :eof

REM Function to create run script
:create_run_script
(
echo @echo off
echo echo Starting Healthcare Microservices...
echo echo.
echo.
echo echo Starting API Gateway on port 8000...
echo start "API Gateway" cmd /k "cd api_gateway && python manage.py runserver 8000"
echo timeout /t 2
echo.
echo echo Starting User Service on port 8001...
echo start "User Service" cmd /k "cd user_service && python manage.py runserver 8001"
echo timeout /t 2
echo.
echo echo Starting Patient Service on port 8002...
echo start "Patient Service" cmd /k "cd patient_service && python manage.py runserver 8002"
echo timeout /t 2
echo.
echo echo Starting Doctor Service on port 8003...
echo start "Doctor Service" cmd /k "cd doctor_service && python manage.py runserver 8003"
echo timeout /t 2
echo.
echo echo Starting Nurse Service on port 8004...
echo start "Nurse Service" cmd /k "cd nurse_service && python manage.py runserver 8004"
echo timeout /t 2
echo.
echo echo Starting Appointment Service on port 8005...
echo start "Appointment Service" cmd /k "cd appointment_service && python manage.py runserver 8005"
echo timeout /t 2
echo.
echo echo Starting Health Record Service on port 8006...
echo start "Health Record Service" cmd /k "cd health_record_service && python manage.py runserver 8006"
echo timeout /t 2
echo.
echo echo Starting Medication Service on port 8007...
echo start "Medication Service" cmd /k "cd medication_service && python manage.py runserver 8007"
echo timeout /t 2
echo.
echo echo Starting Laboratory Service on port 8008...
echo start "Laboratory Service" cmd /k "cd laboratory_service && python manage.py runserver 8008"
echo timeout /t 2
echo.
echo echo Starting Pharmacy Service on port 8009...
echo start "Pharmacy Service" cmd /k "cd pharmacy_service && python manage.py runserver 8009"
echo timeout /t 2
echo.
echo echo Starting Invoice Service on port 8010...
echo start "Invoice Service" cmd /k "cd invoice_service && python manage.py runserver 8010"
echo timeout /t 2
echo.
echo echo Starting Payment Service on port 8011...
echo start "Payment Service" cmd /k "cd payment_service && python manage.py runserver 8011"
echo timeout /t 2
echo.
echo echo Starting Notification Service on port 8012...
echo start "Notification Service" cmd /k "cd notification_service && python manage.py runserver 8012"
echo timeout /t 2
echo.
echo echo Starting Insurance Service on port 8013...
echo start "Insurance Service" cmd /k "cd insurance_service && python manage.py runserver 8013"
echo timeout /t 2
echo.
echo echo Starting Chatbot Service on port 8014...
echo start "Chatbot Service" cmd /k "cd chatbot_service && python manage.py runserver 8014"
echo.
echo echo.
echo echo All services started successfully!
echo echo API Gateway: http://localhost:8000
echo echo User Service: http://localhost:8001
echo echo Patient Service: http://localhost:8002
echo echo Doctor Service: http://localhost:8003
echo echo Nurse Service: http://localhost:8004
echo echo Appointment Service: http://localhost:8005
echo echo Health Record Service: http://localhost:8006
echo echo Medication Service: http://localhost:8007
echo echo Laboratory Service: http://localhost:8008
echo echo Pharmacy Service: http://localhost:8009
echo echo Invoice Service: http://localhost:8010
echo echo Payment Service: http://localhost:8011
echo echo Notification Service: http://localhost:8012
echo echo Insurance Service: http://localhost:8013
echo echo Chatbot Service: http://localhost:8014
echo echo.
echo pause
) > run_all.bat

(
echo @echo off
echo echo Setting up databases for all services...
echo echo.
echo.
echo cd user_service
echo echo Setting up User Service database...
echo python manage.py makemigrations
echo python manage.py migrate
echo cd ..
echo.
echo cd patient_service
echo echo Setting up Patient Service database...
echo python manage.py makemigrations
echo python manage.py migrate
echo cd ..
echo.
echo cd doctor_service
echo echo Setting up Doctor Service database...
echo python manage.py makemigrations
echo python manage.py migrate
echo cd ..
echo.
echo cd nurse_service
echo echo Setting up Nurse Service database...
echo python manage.py makemigrations
echo python manage.py migrate
echo cd ..
echo.
echo cd appointment_service
echo echo Setting up Appointment Service database...
echo python manage.py makemigrations
echo python manage.py migrate
echo cd ..
echo.
echo cd health_record_service
echo echo Setting up Health Record Service database...
echo python manage.py makemigrations
echo python manage.py migrate
echo cd ..
echo.
echo cd medication_service
echo echo Setting up Medication Service database...
echo python manage.py makemigrations
echo python manage.py migrate
echo cd ..
echo.
echo cd laboratory_service
echo echo Setting up Laboratory Service database...
echo python manage.py makemigrations
echo python manage.py migrate
echo cd ..
echo.
echo cd pharmacy_service
echo echo Setting up Pharmacy Service database...
echo python manage.py makemigrations
echo python manage.py migrate
echo cd ..
echo.
echo cd invoice_service
echo echo Setting up Invoice Service database...
echo python manage.py makemigrations
echo python manage.py migrate
echo cd ..
echo.
echo cd payment_service
echo echo Setting up Payment Service database...
echo python manage.py makemigrations
echo python manage.py migrate
echo cd ..
echo.
echo cd notification_service
echo echo Setting up Notification Service database...
echo python manage.py makemigrations
echo python manage.py migrate
echo cd ..
echo.
echo cd insurance_service
echo echo Setting up Insurance Service database...
echo python manage.py makemigrations
echo python manage.py migrate
echo cd ..
echo.
echo cd chatbot_service
echo echo Setting up Chatbot Service database...
echo python manage.py makemigrations
echo python manage.py migrate
echo cd ..
echo.
echo cd api_gateway
echo echo Setting up API Gateway database...
echo python manage.py makemigrations
echo python manage.py migrate
echo cd ..
echo.
echo echo All databases setup completed!
echo pause
) > setup_databases.bat

goto :eof