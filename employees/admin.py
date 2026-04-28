from django.contrib import admin

from .models import Department, Employee


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'full_name', 'job_title', 'department', 'updated_at']
    list_filter = ['department']
    search_fields = ['employee_id', 'full_name', 'job_title']
    ordering = ['full_name']
