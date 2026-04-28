from __future__ import annotations

import csv
import io

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CsvUploadForm, DepartmentForm, EmployeeForm, EmployeeSearchForm
from .models import Department, Employee


@login_required
def employee_list(request: HttpRequest) -> HttpResponse:
    form = EmployeeSearchForm(request.GET or None)
    employees = Employee.objects.select_related('department').all()

    if form.is_valid():
        q = form.cleaned_data.get('q') or ''
        dept = form.cleaned_data.get('department')
        if q:
            employees = employees.filter(
                Q(full_name__icontains=q)
                | Q(job_title__icontains=q)
                | Q(employee_id__icontains=q)
                | Q(department__name__icontains=q)
            )
        if dept:
            employees = employees.filter(department=dept)

    return render(request, 'employees/employee_list.html', {'employees': employees, 'form': form})


@login_required
def employee_detail(request: HttpRequest, pk: int) -> HttpResponse:
    employee = get_object_or_404(Employee.objects.select_related('department'), pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})


@login_required
def employee_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save()
            messages.success(request, 'Employee created.')
            return redirect(employee.get_absolute_url())
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form, 'mode': 'create'})


@login_required
def employee_update(request: HttpRequest, pk: int) -> HttpResponse:
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            employee = form.save()
            messages.success(request, 'Employee updated.')
            return redirect(employee.get_absolute_url())
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form, 'employee': employee, 'mode': 'edit'})


@login_required
def employee_delete(request: HttpRequest, pk: int) -> HttpResponse:
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted.')
        return redirect('employees:list')
    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})


@login_required
def employee_import_csv(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CsvUploadForm(request.POST, request.FILES)
        if form.is_valid():
            raw = form.cleaned_data['csv_file'].read()
            try:
                text = raw.decode('utf-8-sig')
            except UnicodeDecodeError:
                text = raw.decode('cp1252', errors='replace')
            reader = csv.DictReader(io.StringIO(text))

            created = 0
            skipped = 0
            for row in reader:
                full_name = (row.get('full_name') or '').strip()
                job_title = (row.get('job_title') or '').strip()
                dept_name = (row.get('department') or '').strip()
                if not (full_name and job_title and dept_name):
                    skipped += 1
                    continue
                dept, _ = Department.objects.get_or_create(name=dept_name)
                Employee.objects.create(full_name=full_name, job_title=job_title, department=dept)
                created += 1

            messages.success(request, f'Imported {created} employees. Skipped {skipped} rows.')
            return redirect('employees:list')
    else:
        form = CsvUploadForm()

    return render(request, 'employees/employee_import_csv.html', {'form': form, 'csv_template_url': reverse('employees:import_csv')})


@login_required
def department_list(request: HttpRequest) -> HttpResponse:
    departments = Department.objects.all()
    return render(request, 'employees/department_list.html', {'departments': departments})


@login_required
def department_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created.')
            return redirect('employees:departments')
    else:
        form = DepartmentForm()
    return render(request, 'employees/department_form.html', {'form': form})
