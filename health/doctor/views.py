from django.shortcuts import render

# Create your views here.

def index(req):
    username=req.session['username']
    return render(req,'doctor\doctorindex.html',{'doctor_name':username})
# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from users.models import MedicalHistory
from users.models import UserRegister, Appointment
from .models import Doctor
# from users.forms import PrescriptionForm

def doctor_base(request):
    return render(request, 'doctor/doctor_base.html')


def doctor_appointments(request):
    if 'username' in request.session:
        doctor_username = request.session['username']
        doctor = Doctor.objects.get(username=doctor_username)
        
        appointments = Appointment.objects.filter(doctor=doctor)

        return render(request, 'doctor/appointments.html', {'appointments': appointments})
    else:
        return redirect('login')  # Redirect to login if session not found
def medical_history(request):
    # Retrieve medical history of patients
    if 'username' in request.session:
        username = request.session['username']
        doctor = UserRegister.objects.get(username=username)
        medical_histories = MedicalHistory.objects.filter(user__doctor=doctor)
        return render(request, 'doctor/medical_history.html', {'medical_histories': medical_histories})
    else:
        return redirect('login')  # Redirect to login if session not found

# def prescriptions(request):
#     # View prescriptions and provide new prescription functionality
#     if 'username' in request.session:
#         username = request.session['username']
#         doctor = UserRegister.objects.get(username=username)

#         if request.method == 'POST':
#             form = PrescriptionForm(request.POST)
#             if form.is_valid():
#                 prescription = form.save(commit=False)
#                 prescription.doctor = doctor
#                 prescription.save()
#                 messages.success(request, 'Prescription added successfully.')
#                 return redirect('prescriptions')
#         else:
#             form = PrescriptionForm()

#         prescriptions = Prescription.objects.filter(doctor=doctor)
#         return render(request, 'doctor/prescriptions.html', {'prescriptions': prescriptions, 'form': form})
#     else:
#         return redirect('login')  # Redirect to login if session not found

# doctor/views.py

from django.shortcuts import render, redirect
from doctor.models import Doctor
from users.models import Appointment

def doctor_home(request):
    if 'username' in request.session:
        doctor_username = request.session['username']
        doctor = Doctor.objects.get(username=doctor_username)
        
        # Fetch all appointments for the doctor
        all_appointments = Appointment.objects.filter(doctor=doctor)
        
        # Calculate statistics
        total_appointments = all_appointments.count()
        confirmed_appointments = all_appointments.filter(status='Confirmed').count()
        pending_appointments = all_appointments.filter(status='Pending').count()

        return render(request, 'doctor/home.html', {
            'total_appointments': total_appointments,
            'confirmed_appointments': confirmed_appointments,
            'pending_appointments': pending_appointments
        })
    else:
        return redirect('login')  # Redirect to login if session not found

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from users.models import UserRegister, MedicalHistory
from users.forms import MedicalHistoryForm, PrescriptionForm

def patient_list(request):
    patients = UserRegister.objects.all()
    return render(request, 'doctor/patient_list.html', {'patients': patients})

def medical_history(request, patient_id):
    patient = get_object_or_404(UserRegister, pk=patient_id)
    medical_histories = MedicalHistory.objects.filter(user=patient)
    return render(request, 'doctor/medical_history.html', {'patient': patient, 'medical_histories': medical_histories})

def add_medical_history(request, patient_id):
    patient = get_object_or_404(UserRegister, pk=patient_id)
    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            medical_history = form.save(commit=False)
            medical_history.user = patient
            medical_history.save()
            return redirect('medical_history', patient_id=patient_id)
    else:
        form = MedicalHistoryForm()
    return render(request, 'doctor/add_medical_history.html', {'form': form, 'patient': patient})

def prescribe_medication(request, patient_id):
    patient = get_object_or_404(UserRegister, pk=patient_id)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.patient = patient
            prescription.doctor = request.user.doctor  # Assuming request.user is the authenticated doctor
            prescription.save()
            # Add logic to send prescription to pharmacy if needed
            return redirect('doctor_home')  # Redirect to doctor's dashboard
    else:
        form = PrescriptionForm()
    return render(request, 'doctor/prescribe_medication.html', {'form': form, 'patient': patient})
