from __future__ import annotations

import io

import qrcode
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models, transaction
from django.urls import reverse


class Department(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


def employee_photo_upload_to(instance: 'Employee', filename: str) -> str:
    return f'employees/{instance.employee_id or "new"}/photo/{filename}'


def employee_qr_upload_to(instance: 'Employee', filename: str) -> str:
    return f'employees/{instance.employee_id or "new"}/qr/{filename}'


class Employee(models.Model):
    full_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='employees')

    employee_id = models.CharField(max_length=32, unique=True, blank=True, db_index=True)
    photo = models.ImageField(upload_to=employee_photo_upload_to, blank=True, null=True)
    qr_code = models.ImageField(upload_to=employee_qr_upload_to, blank=True, null=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self) -> str:
        return f'{self.full_name} ({self.employee_id or "new"})'

    def get_absolute_url(self) -> str:
        return reverse('employees:detail', kwargs={'pk': self.pk})

    def get_profile_url(self) -> str:
        base = getattr(settings, 'SITE_URL', '').rstrip('/')
        return f'{base}{self.get_absolute_url()}'

    def _build_qr_payload(self) -> str:
        # Prefer profile URL for nicer scanning; fall back to employee ID.
        try:
            return self.get_profile_url()
        except Exception:
            return self.employee_id

    def _generate_qr_png_bytes(self) -> bytes:
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=8,
            border=2,
        )
        qr.add_data(self._build_qr_payload())
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return buf.getvalue()

    def ensure_employee_id(self) -> None:
        """
        Generates a stable human-friendly employee id once the row exists.
        """
        if self.employee_id:
            return
        self.employee_id = f'EMP{self.pk:06d}'

    def ensure_qr_code(self) -> None:
        if not self.employee_id:
            return
        png = self._generate_qr_png_bytes()
        filename = f'{self.employee_id}.png'
        self.qr_code.save(filename, ContentFile(png), save=False)

    def save(self, *args, **kwargs):
        # Ensure a unique employee_id based on PK.
        if self.pk is None and not self.employee_id:
            with transaction.atomic():
                super().save(*args, **kwargs)
                self.ensure_employee_id()
                self.ensure_qr_code()
                super().save(update_fields=['employee_id', 'qr_code', 'updated_at'])
                return

        if self.pk is not None and not self.employee_id:
            self.ensure_employee_id()

        # Refresh QR if missing; keep existing otherwise.
        if not self.qr_code and self.employee_id:
            self.ensure_qr_code()

        return super().save(*args, **kwargs)
