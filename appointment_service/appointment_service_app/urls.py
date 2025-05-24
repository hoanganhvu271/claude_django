from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/appointments/', views.AppointmentListCreateView.as_view(), name='appointment-list'),
    path('api/v1/appointments/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment-detail'),
    path('api/v1/patients/<int:patient_id>/appointments/', views.get_patient_appointments, name='patient-appointments'),
    path('api/v1/doctors/<int:doctor_id>/appointments/', views.get_doctor_appointments, name='doctor-appointments'),
]