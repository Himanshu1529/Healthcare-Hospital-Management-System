"""
URL configuration for Healthcare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views   # Corrected import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path(r'^$',views.signin, name='signin'),
    path('', views.signin, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('doctor/dashboard/', views.doctor_home, name='doctor_home'),
    path('patient/<int:patient_id>/dashboard/', views.patient_home, name='patient_home'),
    path('patient/<int:patient_id>/profile/', views.patient_profile, name='patient_profile'),
    path('patient/<int:patient_id>/billing/', views.patient_billing_info, name='patient_billing_info'),
    path('reception/dashboard/', views.receptionist_home, name='receptionist_home'),
    path('add-userprofile/', views.add_userprofile, name='add_userprofile'),
    path('userprofile/edit/<int:profile_id>/', views.edit_userprofile, name='edit_userprofile'),
    path('userprofile/delete/<int:profile_id>/', views.delete_userprofile, name='delete_userprofile'),
    path('add-patient/', views.add_patient, name='add_patient'),
    path('patient/edit/<int:patient_id>/', views.edit_patient, name='edit_patient'),
    path('patient/delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('billing/edit/<int:billing_id>/', views.edit_patient_billing, name='edit_patient_billing'),
    path('billing/delete/<int:billing_id>/', views.delete_patient_billing, name='delete_patient_billing'),
    path('add_patient_billing/', views.add_patient_billing, name='add_patient_billing'),
    path('about-us/', views.aboutus, name='about'),
    path('doctor/', views.doctors, name='doctors'),
]

