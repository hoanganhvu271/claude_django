from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/health-records/', views.HealthRecordListCreateView.as_view(), name='health-record-list'),
    path('api/v1/health-records/<int:pk>/', views.HealthRecordDetailView.as_view(), name='health-record-detail'),
    path('api/v1/patients/<int:patient_id>/health-records/', views.PatientHealthRecordsView.as_view(), name='patient-health-records'),
    path('api/v1/patients/<int:patient_id>/allergies/', views.PatientAllergiesView.as_view(), name='patient-allergies'),
    path('api/v1/vital-signs/', views.VitalSignsListCreateView.as_view(), name='vital-signs-list'),
    path('api/v1/allergies/', views.AllergyListCreateView.as_view(), name='allergy-list'),
]