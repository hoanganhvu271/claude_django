from rest_framework import generics
from .models import HealthRecord, VitalSigns, Allergy
from .serializers import HealthRecordSerializer, VitalSignsSerializer, AllergySerializer

class HealthRecordListCreateView(generics.ListCreateAPIView):
    queryset = HealthRecord.objects.all()
    serializer_class = HealthRecordSerializer

class HealthRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HealthRecord.objects.all()
    serializer_class = HealthRecordSerializer

class PatientHealthRecordsView(generics.ListAPIView):
    serializer_class = HealthRecordSerializer
    
    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return HealthRecord.objects.filter(patient_id=patient_id).order_by('-visit_date')

class PatientAllergiesView(generics.ListAPIView):
    serializer_class = AllergySerializer
    
    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return Allergy.objects.filter(patient_id=patient_id).order_by('-created_at')

class VitalSignsListCreateView(generics.ListCreateAPIView):
    queryset = VitalSigns.objects.all()
    serializer_class = VitalSignsSerializer

class AllergyListCreateView(generics.ListCreateAPIView):
    queryset = Allergy.objects.all()
    serializer_class = AllergySerializer