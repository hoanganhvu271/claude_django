@echo off
echo Setting up databases for all services...
echo.

cd user_service
echo Setting up User Service database...
python manage.py makemigrations
python manage.py migrate
cd ..

cd patient_service
echo Setting up Patient Service database...
python manage.py makemigrations
python manage.py migrate
cd ..

cd doctor_service
echo Setting up Doctor Service database...
python manage.py makemigrations
python manage.py migrate
cd ..

cd nurse_service
echo Setting up Nurse Service database...
python manage.py makemigrations
python manage.py migrate
cd ..

cd appointment_service
echo Setting up Appointment Service database...
python manage.py makemigrations
python manage.py migrate
cd ..

cd health_record_service
echo Setting up Health Record Service database...
python manage.py makemigrations
python manage.py migrate
cd ..

cd medication_service
echo Setting up Medication Service database...
python manage.py makemigrations
python manage.py migrate
cd ..

cd laboratory_service
echo Setting up Laboratory Service database...
python manage.py makemigrations
python manage.py migrate
cd ..

cd pharmacy_service
echo Setting up Pharmacy Service database...
python manage.py makemigrations
python manage.py migrate
cd ..

cd invoice_service
echo Setting up Invoice Service database...
python manage.py makemigrations
python manage.py migrate
cd ..

cd payment_service
echo Setting up Payment Service database...
python manage.py makemigrations
python manage.py migrate
cd ..

cd notification_service
echo Setting up Notification Service database...
python manage.py makemigrations
python manage.py migrate
cd ..

cd insurance_service
echo Setting up Insurance Service database...
python manage.py makemigrations
python manage.py migrate
cd ..

cd chatbot_service
echo Setting up Chatbot Service database...
python manage.py makemigrations
python manage.py migrate
cd ..

cd api_gateway
echo Setting up API Gateway database...
python manage.py makemigrations
python manage.py migrate
cd ..

echo All databases setup completed!
pause
