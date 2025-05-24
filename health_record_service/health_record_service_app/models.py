from django.db import models

class HealthRecord(models.Model):
    patient_id = models.IntegerField()
    doctor_id = models.IntegerField()
    visit_date = models.DateTimeField()
    chief_complaint = models.TextField()
    history_present_illness = models.TextField()
    physical_examination = models.TextField()
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class VitalSigns(models.Model):
    health_record = models.ForeignKey(HealthRecord, on_delete=models.CASCADE)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    blood_pressure_systolic = models.IntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.IntegerField(null=True, blank=True)
    heart_rate = models.IntegerField(null=True, blank=True)
    respiratory_rate = models.IntegerField(null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

class Allergy(models.Model):
    patient_id = models.IntegerField()
    allergen = models.CharField(max_length=100)
    reaction = models.TextField()
    severity = models.CharField(max_length=20, choices=[
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe')
    ])
    created_at = models.DateTimeField(auto_now_add=True)