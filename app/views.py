from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import *
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from datetime import datetime

# Create your views here.

def index(request):
    return render(request, "main/index.html")


def receptionist_home(request):
    # Total users (excluding superusers if desired)
    total_users = UserProfile.objects.count()
    total_patients = Patient.objects.count()

    # Total pending bills = sum of balance amounts where balance > 0
    pending_bills = PatientBilling.objects.annotate(
        balance=ExpressionWrapper(
            F('total_amount') - F('discount') - F('paid_amount'),
            output_field=DecimalField()
        )
    ).filter(balance__gt=0).aggregate(total_due=Sum('balance'))['total_due'] or 0

    context = {
        'total_users': total_users,
        'total_patients': total_patients,
        'total_pending_bills': pending_bills,
    }
    return render(request, 'reception/index.html', context)

def doctor_home(request):
    if not request.user.is_authenticated:
        return redirect('login') 

    userprofile = UserProfile.objects.get(user=request.user)
    context = {
        'userprofile': userprofile
    }
    return render(request, 'doctor/index.html', context)

def logout_view(request):
    logout(request)  # This will clear the session
    return redirect('login') 


def add_userprofile(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            profiles = UserProfile.objects.all()
            return render(request, 'auth/add_userprofile.html', {
                'error': 'Username already exists!',
                'profiles': profiles
            })

        user = User.objects.create_user(username=username, password=password, email=email)

        # Profile data
        user_type = request.POST.get('user_type')
        user_addr = request.POST.get('user_addr')
        user_mobile = request.POST.get('user_mobile')
        user_hire_date = request.POST.get('user_hire_date')
        user_dob = request.POST.get('user_dob')
        user_specialised = request.POST.get('user_specialised')
        user_sex = request.POST.get('user_sex')
        user_qualification = request.POST.get('user_qualification')
        user_bloodgroup = request.POST.get('user_bloodgroup')

        UserProfile.objects.create(
            user=user,
            user_type=user_type,
            user_addr=user_addr,
            user_mobile=user_mobile,
            user_hire_date=user_hire_date,
            user_dob=user_dob,
            user_specialised=user_specialised,
            user_sex=user_sex,
            user_qualification=user_qualification,
            user_bloodgroup=user_bloodgroup
        )

        return redirect('add_userprofile')

    profiles = UserProfile.objects.all()
    return render(request, 'auth/add_userprofile.html', {'profiles': profiles})


def edit_userprofile(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)

    if request.method == "POST":
        # User fields
        profile.user.username = request.POST.get('username')
        profile.user.first_name = request.POST.get('first_name')
        profile.user.last_name = request.POST.get('last_name')
        profile.user.email = request.POST.get('email')
        profile.user.save()

        # Helper to convert date or None
        def parse_date_or_none(date_str):
            return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        # UserProfile fields
        profile.user_type = request.POST.get('user_type')
        profile.user_addr = request.POST.get('user_addr')
        profile.user_mobile = request.POST.get('user_mobile')
        profile.user_hire_date = parse_date_or_none(request.POST.get('user_hire_date'))
        profile.user_dob = parse_date_or_none(request.POST.get('user_dob'))
        profile.user_specialised = request.POST.get('user_specialised')
        profile.user_sex = request.POST.get('user_sex')
        profile.user_qualification = request.POST.get('user_qualification')
        profile.user_bloodgroup = request.POST.get('user_bloodgroup')
        profile.save()

        return redirect('add_userprofile')

    return render(request, 'auth/edit_userprofile.html', {'profile': profile})

def delete_userprofile(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)

    # Optionally delete the associated user as well
    user = profile.user
    profile.delete()
    user.delete()

    return redirect('add_userprofile') 

def patient_home(request,patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    billings = PatientBilling.objects.filter(patient=patient).order_by('-created_at')

    # Calculate totals
    total_billed = sum(billing.total_amount for billing in billings)
    total_discount = sum(billing.discount for billing in billings)
    total_paid = sum(billing.paid_amount for billing in billings)
    total_due = total_billed - total_discount - total_paid

    context = {
        'patient': patient,
        'billings': billings,
        'total_billed': total_billed,
        'total_discount': total_discount,
        'total_paid': total_paid,
        'total_due': total_due,
    }
    return render(request, 'patient/index.html',context)

def patient_profile(request,patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    context = {
        'patient': patient,
    }
    return render(request, 'patient/profile.html',context)

def add_patient(request):
    if request.method == "POST":
        name = request.POST.get('name')
        father_name = request.POST.get('father_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        bloodgroup = request.POST.get('bloodgroup')
        sex = request.POST.get('sex')
        age = request.POST.get('age')

        # Use phone number as username if email is missing
        username = email if email else phone

        # Validate username (avoid duplicate usernames)
        if User.objects.filter(username=username).exists():
            # You can show a message to the user here
            return redirect('add_patient')

        # Step 1: Create User, password is phone number
        user = User.objects.create_user(
            username=username,
            email=email,
            password=phone,   # ← Set password as phone number
            first_name=name
        )

        # Step 2: Create Patient linked to User
        patient = Patient.objects.create(
            user=user,
            name=name,
            father_name=father_name,
            email=email,
            phone=phone,
            address=address,
            bloodgroup=bloodgroup,
            sex=sex,
            age=age,
        )

        return redirect('add_patient')

    patients = Patient.objects.all()
    return render(request, 'auth/add_patient.html', {'patients': patients})


def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == "POST":
        name = request.POST.get('name')
        father_name = request.POST.get('father_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        bloodgroup = request.POST.get('bloodgroup')
        sex = request.POST.get('sex')
        age = request.POST.get('age')

        # Update related User
        user = patient.user
        user.first_name = name
        user.email = email
        user.username = email if email else phone
        user.set_password(phone)  # If you want to reset password to phone number
        user.save()

        # Update Patient
        patient.name = name
        patient.father_name = father_name
        patient.email = email
        patient.phone = phone
        patient.address = address
        patient.bloodgroup = bloodgroup
        patient.sex = sex
        patient.age = age
        patient.save()

        return redirect('add_patient')  # or your patient list page

    return render(request, 'auth/edit_patient.html', {'patient': patient})


def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    # Delete the linked User
    if patient.user:
        patient.user.delete()

    # Delete the Patient object (will be auto-deleted if User is deleted with on_delete=CASCADE)
    patient.delete()

    return redirect('add_patient')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                userprofile = UserProfile.objects.get(user=user)
                if userprofile.user_type == 'RECEPTIONIST':
                    return HttpResponseRedirect('/reception/dashboard/')
                elif userprofile.user_type == 'DOCTOR':
                    return HttpResponseRedirect('/doctor/dashboard/')
                elif userprofile.user_type == 'PATIENT':
                    # Find the linked Patient object
                    patient = Patient.objects.filter(email=user.email).first()
                    
                    if patient:
                        return HttpResponseRedirect(f'/patient/{patient.id}/dashboard/')
                    else:
                        # If no linked Patient found, redirect to some fallback page
                        return HttpResponseRedirect('/patient/no_profile_found/')
                else:
                    # Default fallback
                    return HttpResponseRedirect('/')
            except UserProfile.DoesNotExist:
                return render(request, 'auth/login.html', {'error': 'User profile not found'})
        else:
            return render(request, 'auth/login.html', {'error': 'Invalid username or password'})
    return render(request, 'auth/login.html')


# views.py
def add_patient_billing(request):
    if request.method == "POST":
        patient_id = request.POST.get('patient')
        total_amount = request.POST.get('total_amount')
        discount = request.POST.get('discount') or 0  # Default to 0 if empty
        paid_amount = request.POST.get('paid_amount')
        payment_method = request.POST.get('payment_method')
        billing_notes = request.POST.get('billing_notes')

        patient = get_object_or_404(Patient, id=patient_id)

        PatientBilling.objects.create(
            patient=patient,
            total_amount=total_amount,
            discount=discount,
            paid_amount=paid_amount,
            payment_method=payment_method,
            billing_notes=billing_notes,
        )

        return redirect('add_patient_billing/')

    patients = Patient.objects.all()
    billings = PatientBilling.objects.select_related('patient').order_by('-created_at')
    return render(request, 'auth/add_patient_billing.html', {'patients': patients, 'billings': billings})


def edit_patient_billing(request, billing_id):
    billing = get_object_or_404(PatientBilling, id=billing_id)

    if request.method == "POST":
        patient_id = request.POST.get('patient')
        total_amount = request.POST.get('total_amount')
        discount = request.POST.get('discount') or 0
        paid_amount = request.POST.get('paid_amount')
        payment_method = request.POST.get('payment_method')
        billing_notes = request.POST.get('billing_notes')

        patient = get_object_or_404(Patient, id=patient_id)

        billing.patient = patient
        billing.total_amount = total_amount
        billing.discount = discount
        billing.paid_amount = paid_amount
        billing.payment_method = payment_method
        billing.billing_notes = billing_notes
        billing.save()

        return redirect('add_patient_billing')

    patients = Patient.objects.all()
    return render(request, 'auth/edit_patient_billing.html', {
        'billing': billing,
        'patients': patients
    })

def delete_patient_billing(request, billing_id):
    billing = get_object_or_404(PatientBilling, id=billing_id)
    billing.delete()
    return redirect('add_patient_billing')

def patient_billing_info(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    billings = PatientBilling.objects.filter(patient=patient).order_by('-bill_date')  # latest bills first

    # Calculate totals
    total_amount = sum(billing.total_amount for billing in billings)
    total_paid = sum(billing.paid_amount for billing in billings)
    total_due = total_amount - total_paid

    context = {
        'patient': patient,
        'billings': billings,
        'total_amount': total_amount,
        'total_paid': total_paid,
        'total_due': total_due,
    }
    return render(request, 'patient/billing_info.html', context)

def aboutus(request):
    return render(request, "main/about.html")

def doctors(request):
    return render(request, "main/doctor.html")