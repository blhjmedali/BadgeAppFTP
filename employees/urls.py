from django.urls import path

from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.employee_list, name='list'),
    path('employees/new/', views.employee_create, name='create'),
    path('employees/<int:pk>/', views.employee_detail, name='detail'),
    path('employees/<int:pk>/edit/', views.employee_update, name='update'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='delete'),
    path('employees/import/csv/', views.employee_import_csv, name='import_csv'),
    path('departments/', views.department_list, name='departments'),
    path('departments/new/', views.department_create, name='department_create'),
]

