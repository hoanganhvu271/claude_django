from django.db import models

class Pharmacy(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    license_number = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    medication_id = models.IntegerField()  # Reference to Medication service
    batch_number = models.CharField(max_length=50)
    expiry_date = models.DateField()
    quantity_in_stock = models.IntegerField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_level = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DispensingRecord(models.Model):
    prescription_id = models.IntegerField()  # Reference to Prescription service
    pharmacist_id = models.IntegerField()
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity_dispensed = models.IntegerField()
    dispensing_date = models.DateTimeField(auto_now_add=True)
    patient_counseled = models.BooleanField(default=False)
    notes = models.TextField(blank=True)