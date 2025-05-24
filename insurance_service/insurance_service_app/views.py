from rest_framework import generics
from .models import InsuranceProvider, InsurancePolicy, InsuranceClaim
from .serializers import InsuranceProviderSerializer, InsurancePolicySerializer, InsuranceClaimSerializer

class InsurancePolicyListCreateView(generics.ListCreateAPIView):
    queryset = InsurancePolicy.objects.all()
    serializer_class = InsurancePolicySerializer

class InsuranceClaimListCreateView(generics.ListCreateAPIView):
    queryset = InsuranceClaim.objects.all()
    serializer_class = InsuranceClaimSerializer

class PatientInsurancePoliciesView(generics.ListAPIView):
    serializer_class = InsurancePolicySerializer
    
    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return InsurancePolicy.objects.filter(patient_id=patient_id, is_active=True)