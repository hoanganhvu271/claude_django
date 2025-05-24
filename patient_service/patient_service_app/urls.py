from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/patients/', views.PatientListCreateView.as_view(), name='patient-list'),
    path('api/v1/patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient-detail'),
]