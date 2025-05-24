@echo off
echo Starting Healthcare Microservices...
echo.

echo Starting API Gateway on port 8000...
start "API Gateway" cmd /k "cd api_gateway && python manage.py runserver 8000"
timeout /t 2

echo Starting User Service on port 8001...
start "User Service" cmd /k "cd user_service && python manage.py runserver 8001"
timeout /t 2

echo Starting Patient Service on port 8002...
start "Patient Service" cmd /k "cd patient_service && python manage.py runserver 8002"
timeout /t 2

echo Starting Doctor Service on port 8003...
start "Doctor Service" cmd /k "cd doctor_service && python manage.py runserver 8003"
timeout /t 2

echo Starting Nurse Service on port 8004...
start "Nurse Service" cmd /k "cd nurse_service && python manage.py runserver 8004"
timeout /t 2

echo Starting Appointment Service on port 8005...
start "Appointment Service" cmd /k "cd appointment_service && python manage.py runserver 8005"
timeout /t 2

echo Starting Health Record Service on port 8006...
start "Health Record Service" cmd /k "cd health_record_service && python manage.py runserver 8006"
timeout /t 2

echo Starting Medication Service on port 8007...
start "Medication Service" cmd /k "cd medication_service && python manage.py runserver 8007"
timeout /t 2

echo Starting Laboratory Service on port 8008...
start "Laboratory Service" cmd /k "cd laboratory_service && python manage.py runserver 8008"
timeout /t 2

echo Starting Pharmacy Service on port 8009...
start "Pharmacy Service" cmd /k "cd pharmacy_service && python manage.py runserver 8009"
timeout /t 2

echo Starting Invoice Service on port 8010...
start "Invoice Service" cmd /k "cd invoice_service && python manage.py runserver 8010"
timeout /t 2

echo Starting Payment Service on port 8011...
start "Payment Service" cmd /k "cd payment_service && python manage.py runserver 8011"
timeout /t 2

echo Starting Notification Service on port 8012...
start "Notification Service" cmd /k "cd notification_service && python manage.py runserver 8012"
timeout /t 2

echo Starting Insurance Service on port 8013...
start "Insurance Service" cmd /k "cd insurance_service && python manage.py runserver 8013"
timeout /t 2

echo Starting Chatbot Service on port 8014...
start "Chatbot Service" cmd /k "cd chatbot_service && python manage.py runserver 8014"

echo.
echo All services started successfully!
echo API Gateway: http://localhost:8000
echo User Service: http://localhost:8001
echo Patient Service: http://localhost:8002
echo Doctor Service: http://localhost:8003
echo Nurse Service: http://localhost:8004
echo Appointment Service: http://localhost:8005
echo Health Record Service: http://localhost:8006
echo Medication Service: http://localhost:8007
echo Laboratory Service: http://localhost:8008
echo Pharmacy Service: http://localhost:8009
echo Invoice Service: http://localhost:8010
echo Payment Service: http://localhost:8011
echo Notification Service: http://localhost:8012
echo Insurance Service: http://localhost:8013
echo Chatbot Service: http://localhost:8014
echo.
pause
