from rest_framework import generics
from .models import LabTest, LabOrder, LabResult
from .serializers import LabTestSerializer, LabOrderSerializer, LabResultSerializer

class LabTestListCreateView(generics.ListCreateAPIView):
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer

class LabOrderListCreateView(generics.ListCreateAPIView):
    queryset = LabOrder.objects.all()
    serializer_class = LabOrderSerializer

class LabResultListCreateView(generics.ListCreateAPIView):
    queryset = LabResult.objects.all()
    serializer_class = LabResultSerializer

class PatientLabResultsView(generics.ListAPIView):
    serializer_class = LabResultSerializer
    
    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return LabResult.objects.filter(lab_order__patient_id=patient_id)