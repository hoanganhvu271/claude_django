from rest_framework import serializers
from .models import (
    ChatSession, ChatMessage, FAQ, Symptom, Disease, DiseaseSymptom,
    DiagnosisSession, ReportedSymptom, ResponseTemplate
)

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'

class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatSession
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = '__all__'

class DiseaseSymptomSerializer(serializers.ModelSerializer):
    symptom = SymptomSerializer(read_only=True)
    
    class Meta:
        model = DiseaseSymptom
        fields = '__all__'

class DiseaseSerializer(serializers.ModelSerializer):
    symptoms_detail = DiseaseSymptomSerializer(source='diseasesymptom_set', many=True, read_only=True)
    
    class Meta:
        model = Disease
        fields = '__all__'

class ReportedSymptomSerializer(serializers.ModelSerializer):
    symptom = SymptomSerializer(read_only=True)
    
    class Meta:
        model = ReportedSymptom
        fields = '__all__'

class DiagnosisSessionSerializer(serializers.ModelSerializer):
    reported_symptoms = ReportedSymptomSerializer(source='reportedsymptom_set', many=True, read_only=True)
    chat_session = ChatSessionSerializer(read_only=True)
    
    class Meta:
        model = DiagnosisSession
        fields = '__all__'

class ResponseTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseTemplate
        fields = '__all__'