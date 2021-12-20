"""Companies models admin."""

# Django
from django.contrib import admin

# Models
from app.companies.models import AccessPoint, AccessHour, Company, Employee


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Company model admin."""

    list_display = [
        'pk', 'nit', 'name',
        'commercial_name', 'admin',
        'web_site', 'email',
        'phone_number', 'direction',
        'country', 'state', 'city',
        'created', 'updated'
    ]

    ordering = ['name', 'commercial_name']


@admin.register(AccessPoint)
class AccessPointAdmin(admin.ModelAdmin):
    """Access Point model admin."""

    list_display = [
        'pk', 'name', 'company',
        'email', 'phone_number',
        'direction', 'country',
        'state', 'city',
        'created', 'updated',
        'geolocation', 'active'
    ]

    ordering = ['name']


@admin.register(AccessHour)
class AccessHourAdmin(admin.ModelAdmin):
    """Access Hour model admin."""

    list_display =[
        'pk', 'access_point',
        'start', 'finish',
        'user', 'active', 
        'created', 'updated'
    ]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Employee model admin."""

    list_display = [
        'pk', 'user', 'company',
        'created', 'updated'
    ]