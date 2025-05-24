from rest_framework import serializers
from .models import Pharmacy, InventoryItem, DispensingRecord

class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = '__all__'

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'

class DispensingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispensingRecord
        fields = '__all__'