from __future__ import annotations

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from employees.models import Department, Employee


class Command(BaseCommand):
    help = 'Seed demo admin + sample departments/employees.'

    def handle(self, *args, **options):
        User = get_user_model()

        username = 'admin'
        password = 'admin123'
        email = 'admin@example.com'

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Created superuser {username} / {password}'))
        else:
            self.stdout.write(self.style.WARNING('Superuser "admin" already exists (skipping).'))

        engineering, _ = Department.objects.get_or_create(name='Engineering')
        hr, _ = Department.objects.get_or_create(name='HR')
        ops, _ = Department.objects.get_or_create(name='Operations')

        samples = [
            ('Amina El Idrissi', 'Backend Engineer', engineering),
            ('Youssef Benali', 'HR Specialist', hr),
            ('Sara Moukhtar', 'Operations Coordinator', ops),
        ]

        created = 0
        for full_name, job_title, dept in samples:
            if Employee.objects.filter(full_name=full_name, job_title=job_title, department=dept).exists():
                continue
            Employee.objects.create(full_name=full_name, job_title=job_title, department=dept)
            created += 1

        self.stdout.write(self.style.SUCCESS(f'Seeded {created} sample employees.'))

