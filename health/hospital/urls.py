from django.urls import path
from .  import views

urlpatterns = [
    path('',views.adminHome,name='adminhome'),


    path('departments/', views.department_list, name='department_list'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('departments/add/', views.add_department, name='add_department'),
    path('doctors/add/', views.add_doctor, name='add_doctor'),
    path('departments/update/<int:pk>/', views.update_department, name='update_department'),
    path('doctors/update/<int:pk>/', views.update_doctor, name='update_doctor'),
    path('users/', views.user_list, name='user_list'),
    path('user_update/<int:id>/',views.update_user,name='update_user'),
    path('health-resources/', views.health_resource_list, name='health_resource_list'),
    path('health-resources/add/', views.add_health_resource, name='add_health_resource'),
    path('health-resources/<int:pk>/update/', views.update_health_resource, name='update_health_resource'),
    path('health-resources/<int:pk>/delete/', views.delete_health_resource, name='delete_health_resource'),

]

