from django.db import models

class LabTest(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    sample_type = models.CharField(max_length=50)  # blood, urine, etc.
    reference_range = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class LabOrder(models.Model):
    STATUS_CHOICES = [
        ('ordered', 'Ordered'),
        ('collected', 'Sample Collected'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    patient_id = models.IntegerField()
    doctor_id = models.IntegerField()
    lab_test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ordered')
    priority = models.CharField(max_length=20, choices=[
        ('routine', 'Routine'),
        ('urgent', 'Urgent'),
        ('stat', 'STAT'),
    ], default='routine')
    clinical_notes = models.TextField(blank=True)

class LabResult(models.Model):
    lab_order = models.OneToOneField(LabOrder, on_delete=models.CASCADE)
    technician_id = models.IntegerField()
    result_value = models.TextField()
    unit = models.CharField(max_length=20)
    reference_range = models.CharField(max_length=100)
    abnormal_flag = models.CharField(max_length=10, blank=True)
    comments = models.TextField(blank=True)
    result_date = models.DateTimeField(auto_now_add=True)
    verified_by = models.IntegerField(null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)