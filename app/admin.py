from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','user_type', 'user_specialised', 'user_sex')
    search_fields = ('user', 'user_type', 'user_specialised')
    list_filter = ('user_type', 'user_specialised')
      
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name','sex', 'age', 'address')
    search_fields = ('name', 'address')
    list_filter = ('age', 'address','bloodgroup')
    
    
@admin.register(PatientBilling)
class PatientBillingAdmin(admin.ModelAdmin):
    list_display = ('patient','bill_date', 'total_amount')
    search_fields = ('patient', 'bill_date')
    list_filter = ('payment_method', 'bill_date')
    
    
