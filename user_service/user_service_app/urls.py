from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/users/register/', views.register_user, name='register'),
    path('api/v1/users/login/', views.login_user, name='login'),
    path('api/v1/users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
]