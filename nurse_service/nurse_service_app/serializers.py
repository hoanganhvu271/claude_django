from rest_framework import serializers
from .models import Nurse, NursePatientAssignment, CareActivity

class NurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nurse
        fields = '__all__'

class NursePatientAssignmentSerializer(serializers.ModelSerializer):
    nurse = NurseSerializer(read_only=True)
    
    class Meta:
        model = NursePatientAssignment
        fields = '__all__'

class CareActivitySerializer(serializers.ModelSerializer):
    nurse = NurseSerializer(read_only=True)
    
    class Meta:
        model = CareActivity
        fields = '__all__'