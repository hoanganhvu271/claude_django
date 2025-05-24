from django.db import models

class Nurse(models.Model):
    user_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    specialization = models.CharField(max_length=100, blank=True)
    experience_years = models.IntegerField()
    shift = models.CharField(max_length=20, choices=[
        ('day', 'Day Shift'),
        ('night', 'Night Shift'),
        ('rotating', 'Rotating'),
    ])
    department = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nurse {self.first_name} {self.last_name}"

class NursePatientAssignment(models.Model):
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    patient_id = models.IntegerField()
    assigned_date = models.DateTimeField(auto_now_add=True)
    shift_date = models.DateField()
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

class CareActivity(models.Model):
    ACTIVITY_CHOICES = [
        ('vital_signs', 'Vital Signs Check'),
        ('medication', 'Medication Administration'),
        ('wound_care', 'Wound Care'),
        ('patient_education', 'Patient Education'),
        ('assistance', 'Patient Assistance'),
        ('monitoring', 'Patient Monitoring'),
    ]
    
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    patient_id = models.IntegerField()
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    description = models.TextField()
    performed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)