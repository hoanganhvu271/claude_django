from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chatbot_service_app.urls')),  # Đổi từ 'medical_app.urls' thành 'chatbot_service_app.urls'
]