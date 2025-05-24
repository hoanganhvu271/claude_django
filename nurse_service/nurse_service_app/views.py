from rest_framework import generics
from .models import Nurse, NursePatientAssignment, CareActivity
from .serializers import NurseSerializer, NursePatientAssignmentSerializer, CareActivitySerializer

class NurseListCreateView(generics.ListCreateAPIView):
    queryset = Nurse.objects.all()
    serializer_class = NurseSerializer

class NurseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Nurse.objects.all()
    serializer_class = NurseSerializer

class NursePatientAssignmentView(generics.ListCreateAPIView):
    serializer_class = NursePatientAssignmentSerializer
    
    def get_queryset(self):
        nurse_id = self.kwargs.get('nurse_id')
        if nurse_id:
            return NursePatientAssignment.objects.filter(nurse_id=nurse_id, is_active=True)
        return NursePatientAssignment.objects.filter(is_active=True)

class CareActivityListCreateView(generics.ListCreateAPIView):
    queryset = CareActivity.objects.all()
    serializer_class = CareActivitySerializer