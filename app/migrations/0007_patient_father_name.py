# Generated by Django 5.2 on 2025-04-29 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_patient_patientbilling'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='father_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
