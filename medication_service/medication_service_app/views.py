from rest_framework import generics
from .models import Medication, Prescription, PrescriptionItem
from .serializers import MedicationSerializer, PrescriptionSerializer, PrescriptionItemSerializer

class MedicationListCreateView(generics.ListCreateAPIView):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer

class PrescriptionListCreateView(generics.ListCreateAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

class PatientPrescriptionsView(generics.ListAPIView):
    serializer_class = PrescriptionSerializer
    
    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return Prescription.objects.filter(patient_id=patient_id)