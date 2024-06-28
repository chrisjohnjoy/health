from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from .forms import AppointmentForm
from .models import UserRegister,loginTable,Appointment,HealthResource
from doctor.models import Doctor
import stripe


# Create your views here.
def index(req):
    return render(req,'index.html')


def UserRegistration(request):
    if request.method == 'POST':
        userprofile = UserRegister(
            name=request.POST.get('name', ''),
            address=request.POST.get('address', ''),
            place=request.POST.get('place', ''),
            district=request.POST.get('district', ''),
            state=request.POST.get('state', ''),
            pincode=request.POST.get('pincode', ''),
            phone=request.POST.get('phone', ''),
            email=request.POST.get('email', ''),
            username=request.POST.get('username', ''),
            password=request.POST.get('password', ''),
            password2=request.POST.get('password1', '')
        )

        login_table = loginTable(
            username=request.POST.get('username', ''),
            password=request.POST.get('password', ''),
            password2=request.POST.get('password1', ''),
            type='user'
        )

        if userprofile.password == userprofile.password2:
            userprofile.save()
            login_table.save()
            messages.success(request, 'Registration successful')
            return redirect('index')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('index')

    return render(request, 'user/register.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import loginTable  # Adjust the import according to your project structure

def loginPage(req):
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        
        try:
            user = loginTable.objects.filter(username=username, password=password).first()
            
            if user is not None:
                user_name = user.username
                user_type = user.type
                
                req.session['username'] = user_name
                if user_type == 'user':
                    return redirect('userhome')
                elif user_type == 'admin':
                    return redirect('adminhome')
                elif user_type == 'doctor':
                    return redirect('doctorhome')
                else:
                    messages.error(req, 'Invalid role')
            else:
                messages.error(req, 'Invalid username or password')
        except Exception as e:
            messages.error(req, 'An error occurred: ' + str(e))
            
    return render(req, 'User/login.html')

    
def logOut(request):
    logout(request)
    return redirect('login')

def userHome(request):
    user_name=request.session['username']
    return render(request,'User/home.html',{'user_name':user_name})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import AppointmentForm
from .models import UserRegister, Appointment

def appointment_list(request):
    # Retrieve username from session
    username = request.session.get('username')
    if username:
        user = UserRegister.objects.filter(username=username).first()
        if user:
            appointments = Appointment.objects.filter(user=user)
            return render(request, 'User/appointment_list.html', {'appointments': appointments})
        else:
            messages.error(request, 'User not found.')
    else:
        messages.error(request, 'User not authenticated.')
    return redirect('login')  # Redirect to login page or handle accordingly

def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            username = request.session.get('username')
            if username:
                user = UserRegister.objects.filter(username=username).first()
                if user:
                    appointment = form.save(commit=False)
                    appointment.user = user
                    appointment.save()
                    return redirect('appointment_list')
                else:
                    messages.error(request, 'User not found.')
            else:
                messages.error(request, 'User not authenticated.')
    else:
        form = AppointmentForm()
    return render(request, 'User/book_appointment.html', {'form': form})

def edit_appointment(request, pk):
    username = request.session.get('username')
    if username:
        user = UserRegister.objects.filter(username=username).first()
        if user:
            appointment = get_object_or_404(Appointment, pk=pk, user=user)
            if request.method == 'POST':
                form = AppointmentForm(request.POST, instance=appointment)
                if form.is_valid():
                    form.save()
                    return redirect('appointment_list')
            else:
                form = AppointmentForm(instance=appointment)
            return render(request, 'User/book_appointment.html', {'form': form})
        else:
            messages.error(request, 'User not found.')
    else:
        messages.error(request, 'User not authenticated.')
    return redirect('login')  # Redirect to login page or handle accordingly

def delete_appointment(request, pk):
    username = request.session.get('username')
    if username:
        user = UserRegister.objects.filter(username=username).first()
        if user:
            appointment = get_object_or_404(Appointment, pk=pk, user=user)
            if request.method == 'POST':
                appointment.delete()
                return redirect('appointment_list')
            return render(request, 'User/delete_appointment.html', {'appointment': appointment})
        else:
            messages.error(request, 'User not found.')
    else:
        messages.error(request, 'User not authenticated.')
    return redirect('login')  # Redirect to login page or handle accordingly

def health_resource_list(request):
    username = request.session.get('username')

    resources = HealthResource.objects.all()
    return render(request, 'User/health_resources_list.html', {'resources': resources,'user_name':username})



def doctor_list(request):
    username = request.session.get('username')

    doctors = Doctor.objects.all()
    return render(request, 'User/doctor_list.html', {'doctors': doctors,'user_name':username})

# views.py

from django.shortcuts import render
from .models import MedicalHistory

def medical_history(request):
    if 'username' not in request.session:
        return redirect('login')
    user_name = request.session['username']
    user = UserRegister.objects.get(username=user_name)
    medical_histories = MedicalHistory.objects.filter(user=user)
    return render(request, 'User/medical_history.html', {'medical_histories': medical_histories})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .forms import AppointmentForm
from .models import UserRegister, Appointment
from doctor.models import Doctor
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def appointment_list(request):
    username = request.session.get('username')
    if username:
        user = UserRegister.objects.filter(username=username).first()
        if user:
            appointments = Appointment.objects.filter(user=user)
            return render(request, 'User/appointment_list.html', {'appointments': appointments})
        else:
            messages.error(request, 'User not found.')
    else:
        messages.error(request, 'User not authenticated.')
    return redirect('login')

def create_checkout_session(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': f'Appointment with Dr. {appointment.doctor.first_name}',
                },
                'unit_amount': 5000,  # amount in cents, e.g., $50.00
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/success/') + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri('/cancel/'),
        metadata={'appointment_id': appointment.id}  # Add the appointment ID as metadata

    )
    return redirect(session.url, code=303)

def payment_success(request):
    session_id = request.GET.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)
    appointment_id = session.metadata.appointment_id
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'Confirmed'
    appointment.save()
    messages.success(request, 'Payment successful and appointment confirmed.')
    return redirect('appointment_list')

def payment_cancel(request):
    messages.error(request, 'Payment was canceled.')
    return redirect('appointment_list')
# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import AppointmentForm
from .models import UserRegister, Appointment
from doctor.models import Doctor

def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            username = request.session.get('username')
            if username:
                user = UserRegister.objects.filter(username=username).first()
                if user:
                    appointment = form.save(commit=False)
                    appointment.user = user
                    appointment.save()
                    messages.success(request, 'Appointment booked successfully.')
                    return redirect('appointment_list')
                else:
                    messages.error(request, 'User not found.')
            else:
                messages.error(request, 'User not authenticated.')
        else:
            messages.error(request, 'Form is not valid.')
    else:
        form = AppointmentForm()
    
    doctors = Doctor.objects.all()
    return render(request, 'User/book_appointment.html', {'form': form, 'doctors': doctors})

def edit_appointment(request, pk):
    username = request.session.get('username')
    if username:
        user = UserRegister.objects.filter(username=username).first()
        if user:
            appointment = get_object_or_404(Appointment, pk=pk, user=user)
            if request.method == 'POST':
                form = AppointmentForm(request.POST, instance=appointment)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Appointment updated successfully.')
                    return redirect('appointment_list')
            else:
                form = AppointmentForm(instance=appointment)
            
            doctors = Doctor.objects.all()
            return render(request, 'User/edit_appointment.html', {'form': form, 'appointment': appointment, 'doctors': doctors})
        else:
            messages.error(request, 'User not found.')
    else:
        messages.error(request, 'User not authenticated.')
    
    return redirect('login')
