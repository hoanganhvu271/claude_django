from rest_framework import serializers
from .models import HealthRecord, VitalSigns, Allergy

class VitalSignsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalSigns
        fields = '__all__'

class HealthRecordSerializer(serializers.ModelSerializer):
    vital_signs = VitalSignsSerializer(many=True, read_only=True)
    
    class Meta:
        model = HealthRecord
        fields = '__all__'

class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = '__all__'