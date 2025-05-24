cd user_service
@REM del user_service_app\migrations\0*.py
@REM mysql -u root -p
@REM DROP DATABASE IF EXISTS user_service_db;
@REM CREATE DATABASE user_service_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
@REM exit

@REM # Bước 4: Migration lại
python manage.py makemigrations user_service_app
python manage.py migrate

@REM # Bước 5: Kiểm tra
python manage.py showmigrations
python manage.py runserver 8001