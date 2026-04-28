from django.urls import path

from . import views

app_name = 'badges'

urlpatterns = [
    path('employee/<int:pk>/', views.badge_preview, name='preview'),
    path('employee/<int:pk>/pdf/', views.badge_pdf, name='pdf'),
    path('export/pdf/', views.badge_bulk_pdf, name='bulk_pdf'),
]

