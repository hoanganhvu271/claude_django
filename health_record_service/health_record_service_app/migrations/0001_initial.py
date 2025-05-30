# Generated by Django 4.2.7 on 2025-05-24 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Allergy",
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
                ("patient_id", models.IntegerField()),
                ("allergen", models.CharField(max_length=100)),
                ("reaction", models.TextField()),
                (
                    "severity",
                    models.CharField(
                        choices=[
                            ("mild", "Mild"),
                            ("moderate", "Moderate"),
                            ("severe", "Severe"),
                        ],
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="HealthRecord",
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
                ("patient_id", models.IntegerField()),
                ("doctor_id", models.IntegerField()),
                ("visit_date", models.DateTimeField()),
                ("chief_complaint", models.TextField()),
                ("history_present_illness", models.TextField()),
                ("physical_examination", models.TextField()),
                ("diagnosis", models.TextField()),
                ("treatment_plan", models.TextField()),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="VitalSigns",
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
                (
                    "temperature",
                    models.DecimalField(
                        blank=True, decimal_places=1, max_digits=4, null=True
                    ),
                ),
                ("blood_pressure_systolic", models.IntegerField(blank=True, null=True)),
                (
                    "blood_pressure_diastolic",
                    models.IntegerField(blank=True, null=True),
                ),
                ("heart_rate", models.IntegerField(blank=True, null=True)),
                ("respiratory_rate", models.IntegerField(blank=True, null=True)),
                (
                    "weight",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "height",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                ("recorded_at", models.DateTimeField(auto_now_add=True)),
                (
                    "health_record",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="health_record_service_app.healthrecord",
                    ),
                ),
            ],
        ),
    ]
