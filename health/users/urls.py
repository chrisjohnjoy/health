from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.index,name='index'),
    path('login/',views.loginPage,name='login'),
    path('register/',views.UserRegistration,name='register'),
    path('logout/',views.logOut,name='logout'),
    path('userHome/',views.userHome,name='userhome'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/book/', views.book_appointment, name='book_appointment'),
    path('appointments/edit/<int:pk>/', views.edit_appointment, name='edit_appointment'),
    path('appointments/delete/<int:pk>/', views.delete_appointment, name='delete_appointment'),
    path('resources/', views.health_resource_list, name='health_resource_list_user'),
    path('doctor_list',views.doctor_list,name='doctor_list_user'),
    path('medical_history/', views.medical_history, name='medical_history'),
     path('create-checkout-session/<int:pk>/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),


]



