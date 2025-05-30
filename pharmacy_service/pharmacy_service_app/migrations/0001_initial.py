# Generated by Django 4.2.7 on 2025-05-24 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Pharmacy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("address", models.TextField()),
                ("phone", models.CharField(max_length=15)),
                ("email", models.EmailField(max_length=254)),
                ("license_number", models.CharField(max_length=50, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="InventoryItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("medication_id", models.IntegerField()),
                ("batch_number", models.CharField(max_length=50)),
                ("expiry_date", models.DateField()),
                ("quantity_in_stock", models.IntegerField()),
                ("cost_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("selling_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("reorder_level", models.IntegerField(default=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "pharmacy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pharmacy_service_app.pharmacy",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DispensingRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("prescription_id", models.IntegerField()),
                ("pharmacist_id", models.IntegerField()),
                ("quantity_dispensed", models.IntegerField()),
                ("dispensing_date", models.DateTimeField(auto_now_add=True)),
                ("patient_counseled", models.BooleanField(default=False)),
                ("notes", models.TextField(blank=True)),
                (
                    "inventory_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pharmacy_service_app.inventoryitem",
                    ),
                ),
            ],
        ),
    ]
