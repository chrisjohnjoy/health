from django import forms
from .models import HealthResource
from .models import Appointment

class HealthResourceForm(forms.ModelForm):
    class Meta:
        model = HealthResource
        fields = ['title', 'description', 'url']


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
        }

from django import forms
from .models import MedicalHistory, Prescription

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['diagnosis', 'medications', 'allergies', 'treatment']

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medications', 'instructions']
