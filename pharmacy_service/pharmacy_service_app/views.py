from rest_framework import generics
from .models import Pharmacy, InventoryItem, DispensingRecord
from .serializers import PharmacySerializer, InventoryItemSerializer, DispensingRecordSerializer

class PharmacyListCreateView(generics.ListCreateAPIView):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer

class InventoryItemListCreateView(generics.ListCreateAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer

class DispensingRecordListCreateView(generics.ListCreateAPIView):
    queryset = DispensingRecord.objects.all()
    serializer_class = DispensingRecordSerializer