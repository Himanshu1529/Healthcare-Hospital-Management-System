from django.db import models
from django.contrib.auth.models import User

USER_TYPE = (
    ('DOCTOR', 'DOCTOR'),
    ('RECEPTIONIST', 'RECEPTIONIST'),
    ('PATIENT', 'PATIENT'),  # Add this
)
USER_SPECIALISED = (('EMPLANT', 'EMPLANT'), ('ORTHO', 'ORTHO'))
USER_GENDER = (('MALE', 'MALE'), ('FEMALE', 'FEMALE'))
# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	user_type = models.CharField(max_length=15, choices=USER_TYPE, default='PATIENT')
	user_addr = models.CharField(max_length=155, null=True )
	user_mobile = models.IntegerField(null=True )
	user_hire_date = models.DateField(blank=True, null=True)
	user_dob = models.DateField(blank=True, null=True)
	user_specialised = models.CharField(max_length=15, choices=USER_SPECIALISED, blank=True, null=True)
	user_sex = models.CharField(max_length=10, choices=USER_GENDER, default='MALE')
	user_qualification = models.CharField(max_length=100, blank=True, null=True)
	user_bloodgroup = models.CharField(max_length=10, blank=True, null=True)
	def __str__(self):
		return str(self.user.username)


class Patient(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
	name = models.CharField(max_length=100)
	father_name = models.CharField(max_length=100)
	email = models.EmailField(max_length=100, blank=True, null=True)
	phone = models.CharField(max_length=20, blank=True, null=True)
	address = models.CharField(max_length=200, blank=True, null=True)
	bloodgroup = models.CharField(max_length=10, blank=True, null=True)
	sex = models.CharField(max_length=10, choices=USER_GENDER, default='MALE')
	age = models.IntegerField(blank=True, null=True)
	created_at = models.DateField(auto_now_add=True, blank=True, null=True)
	updated_at = models.DateField(auto_now=True, blank=True, null=True)

	def __str__(self):
		return str(self.name)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		# Automatically create or update UserProfile
		UserProfile.objects.update_or_create(
			user=self.user,
			defaults={
				'user_type': 'PATIENT',
				'user_addr': self.address,
				'user_mobile': self.phone if self.phone else None,
				'user_dob': None,
				'user_sex': self.sex,
				'user_bloodgroup': self.bloodgroup,
			}
		)



class PatientBilling(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='billings')
    bill_date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ('CASH', 'Cash'),
            ('CARD', 'Card'),
            ('UPI', 'UPI'),
            ('ONLINE', 'Online Transfer')
        ],
        default='CASH'
    )
    billing_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def balance_amount(self):
        return self.total_amount - self.discount - self.paid_amount

    def __str__(self):
        return f"Bill for {self.patient.name} on {self.bill_date}"