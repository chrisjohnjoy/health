from django.db import models
from hospital.models import Department
# Create your models here.

class Doctor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    experience_years = models.IntegerField(default=0)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='doctors/', blank=True, null=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    password1 = models.CharField(max_length=50)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
