from django.contrib import admin
from django.urls import path, include
from gateway import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/register/', views.register_user, name='register'),
    path('api/v1/users/login/', views.login_user, name='login'),
    path('api/v1/patients/', views.patients, name='patients'),
    path('api/v1/doctors/', views.doctors, name='doctors'),
    path('api/v1/appointments/', views.appointments, name='appointments'),
    path('api/v1/chatbot/', include('gateway.chatbot_urls')),
]
