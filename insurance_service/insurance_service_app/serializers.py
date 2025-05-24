from rest_framework import serializers
from .models import InsuranceProvider, InsurancePolicy, InsuranceClaim

class InsuranceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceProvider
        fields = '__all__'

class InsurancePolicySerializer(serializers.ModelSerializer):
    provider = InsuranceProviderSerializer(read_only=True)
    
    class Meta:
        model = InsurancePolicy
        fields = '__all__'

class InsuranceClaimSerializer(serializers.ModelSerializer):
    policy = InsurancePolicySerializer(read_only=True)
    
    class Meta:
        model = InsuranceClaim
        fields = '__all__'