from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/doctors/', views.DoctorListCreateView.as_view(), name='doctor-list'),
    path('api/v1/doctors/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor-detail'),
    path('api/v1/doctors/<int:doctor_id>/availability/', views.DoctorAvailabilityView.as_view(), name='doctor-availability'),
]