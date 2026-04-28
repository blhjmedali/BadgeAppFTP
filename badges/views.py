from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string

from employees.models import Employee

from .pdf import render_to_pdf


@login_required
def badge_preview(request: HttpRequest, pk: int) -> HttpResponse:
    employee = get_object_or_404(Employee.objects.select_related('department'), pk=pk)
    return render(request, 'badges/badge_preview.html', {'employee': employee})


@login_required
def badge_pdf(request: HttpRequest, pk: int) -> HttpResponse:
    employee = get_object_or_404(Employee.objects.select_related('department'), pk=pk)
    html = render_to_string('badges/badge_pdf_single.html', {'employee': employee, 'request': request})
    return render_to_pdf(html=html, filename=f'{employee.employee_id}_badge.pdf')


@login_required
def badge_bulk_pdf(request: HttpRequest) -> HttpResponse:
    ids = request.GET.getlist('id')
    if ids:
        employees = Employee.objects.select_related('department').filter(pk__in=ids)
    else:
        employees = Employee.objects.select_related('department').all()
    html = render_to_string('badges/badge_pdf_bulk.html', {'employees': employees, 'request': request})
    return render_to_pdf(html=html, filename='employee_badges.pdf')
