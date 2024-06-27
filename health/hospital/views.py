from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from users.models import loginTable,UserRegister,HealthResource
from users.forms import HealthResourceForm
from doctor.models import *
from django.contrib import messages


# Create your views here.
def adminHome(req):
    user_name=req.session['username']
    return render(req,'admin_user/index.html')


def department_list(request):
    departments = Department.objects.all()
    return render(request, 'admin_user/department_list.html', {'departments': departments})

def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'admin_user/doctor_list.html', {'doctors': doctors})
def add_department(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')  # Note: Use request.FILES for file uploads

        department = Department(name=name, description=description, image=image)
        department.save()
        return redirect('department_list')
    return render(request, 'admin_user/department_form.html')

def update_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.name = request.POST.get('name')
        department.description = request.POST.get('description')
        department.image = request.FILES.get('image')

        department.save()
        return redirect('department_list')
    return render(request, 'admin_user/department_form.html', {'department': department})


# Views for handling doctor operations
def add_doctor(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        department_id = request.POST.get('department')  # Assuming 'department' is the ID
        department = Department.objects.get(pk=department_id)
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        specialization = request.POST.get('specialization')
        experience_years = request.POST.get('experience_years')
        bio = request.POST.get('bio')
        image = request.FILES.get('image')
        username = request.POST.get('username')
        password = request.POST.get('password')
        conpass= request.POST.get('password1')

       
        doctor = Doctor(first_name=first_name, last_name=last_name, department=department, email=email,
                        phone_number=phone_number, specialization=specialization, experience_years=experience_years,
                        bio=bio, image=image,username=username, password=password, password1=conpass)
        
        user = loginTable(
            username = request.POST.get('username'''),
            password = request.POST.get('password',''),
            password2 = request.POST.get('password1',''),
            type = 'doctor')
        
        if doctor.password == doctor.password1 :
            doctor.save()
            user.save()
            messages.success(request,'Registraion successfull')
        else:
            messages.error(request,'Registration not sucessfull')
        return redirect('doctor_list')
    departments = Department.objects.all()
    return render(request, 'admin_user/doctor_form.html', {'departments': departments})

def update_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.first_name = request.POST.get('first_name')
        doctor.last_name = request.POST.get('last_name')
        department_id = request.POST.get('department')  # Assuming 'department' is the ID
        doctor.department = Department.objects.get(pk=department_id)
        doctor.email = request.POST.get('email')
        doctor.phone_number = request.POST.get('phone_number')
        doctor.specialization = request.POST.get('specialization')
        doctor.experience_years = request.POST.get('experience_years')
        doctor.bio = request.POST.get('bio')
        doctor.image = request.FILES.get('image')
        doctor.username

        

        doctor.save()
        return redirect('doctor_list')
    departments = Department.objects.all()
    return render(request, 'admin_user/doctor_form.html', {'doctor': doctor, 'departments': departments})

def update_user(req,id):
    user_main = UserRegister.objects.get(id=id)
    if req.method == 'POST':
        user_main.name=req.POST.get('name')
        user_main.address=req.POST.get('address')
        user_main.place=req.POST.get('place')
        user_main.district=req.POST.get('district')
        user_main.state=req.POST.get('state')
        user_main.pincode=req.POST.get('pincode')
        user_main.phone=req.POST.get('phone')
        user_main.email=req.POST.get('email')
        user_main.username=req.POST.get('username')

        user_main.save()
        return redirect('user_list')
    return render(req, 'admin_user/user_update.html',{'user':user_main})


def user_list(request):
    users = UserRegister.objects.all()
    return render(request, 'admin_user/user_list.html', {'users': users})



def health_resource_list(request):
    resources = HealthResource.objects.all()
    return render(request, 'admin_user/health_resource_list.html', {'resources': resources})

def add_health_resource(request):
    if request.method == 'POST':
        form = HealthResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('health_resource_list')
    else:
        form = HealthResourceForm()
    return render(request, 'admin_user/health_resource_form.html', {'form': form})

def update_health_resource(request, pk):
    resource = get_object_or_404(HealthResource, pk=pk)
    if request.method == 'POST':
        form = HealthResourceForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            return redirect('health_resource_list')
    else:
        form = HealthResourceForm(instance=resource)
    return render(request, 'admin_user/health_resource_form.html', {'form': form})

def delete_health_resource(request, pk):
    resource = get_object_or_404(HealthResource, pk=pk)
    if request.method == 'POST':
        resource.delete()
        messages.success(request, 'Resource deleted successfully')
        return redirect('health_resource_list')
    
    return render(request, 'user/health_resource_confirm_delete.html', {'resource': resource})