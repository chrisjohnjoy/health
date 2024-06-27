from django.db import models

# Create your models here.

from doctor.models import Doctor

class UserRegister(models.Model):
    name=models.CharField(max_length=200)
    address=models.CharField(max_length=5000)
    place=models.CharField(max_length=200)
    district=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    pincode=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    password2 = models.CharField(max_length=200, default='') 

    def __str__(self):
        return '{}'.format(self.name)
    
class loginTable(models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    password2 = models.CharField(max_length=200, default='')  # Example default value

    type=models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.username)    # Create your models here.

class HealthResource(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()

    def __str__(self):
        return self.title
   
class Appointment(models.Model):
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.name} on {self.date} at {self.time}"

class MedicalHistory(models.Model):
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    medications = models.TextField()
    allergies = models.TextField()
    treatment = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Medical History for {self.user.name} on {self.date}"