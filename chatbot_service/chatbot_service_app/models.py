from django.db import models
import json
import numpy as np

class Disease(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=100)
    severity_level = models.CharField(max_length=20)  # mild, medium, severe, emergency
    recommendations = models.TextField()
    
    def __str__(self):
        return self.name

class Symptom(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=100)
    is_critical = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class DiseaseSymptom(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    probability = models.FloatField()  # 0-1
    importance = models.FloatField()   # weight for training
    
    class Meta:
        unique_together = ['disease', 'symptom']

class KnowledgeBase(models.Model):
    content = models.TextField()
    topic = models.CharField(max_length=200)
    embedding = models.TextField()  # JSON vector
    confidence = models.FloatField()
    source_type = models.CharField(max_length=50)
    
    def set_embedding(self, vector):
        self.embedding = json.dumps(vector.tolist())
    
    def get_embedding(self):
        return np.array(json.loads(self.embedding)) if self.embedding else None