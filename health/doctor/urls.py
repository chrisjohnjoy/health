from django.urls import path
from . import views

urlpatterns = [
    path('doctor/',views.index,name='doctorhome'),
    path('appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('medical_history/', views.medical_history, name='medical_history'),
    path('home/', views.doctor_home, name='doctor_home'),  # Doctor's dashboard/home page
    path('patients/', views.patient_list, name='patient_list'),
    path('patient/<int:patient_id>/medical_history/', views.medical_history, name='medical_history'),
    path('patient/<int:patient_id>/add_medical_history/', views.add_medical_history, name='add_medical_history'),
    path('patient/<int:patient_id>/prescribe_medication/', views.prescribe_medication, name='prescribe_medication'),

]

