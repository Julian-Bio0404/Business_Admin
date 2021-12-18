"""Company models."""

# Django
from django.core.validators import RegexValidator
from django.db import models

# Utils
from app.utils.models import AppModel


class Company(AppModel):
    """Company model."""

    nit_regex = RegexValidator(
        regex=r"^\d{9,12}$", message='Nit number must has 9-12 digitis')

    nit = models.CharField(validators=[nit_regex], max_length=12)
    name = models.CharField(max_length=80)
    commercial_name = models.CharField(max_length=60)

    admin = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL, null=True, related_name='administrator')

    web_site = models.URLField(
        help_text='personal web site', max_length=200, blank=True)

    employees = models.ManyToManyField(
        'users.User', through='companies.Employee',
        through_fields=('company', 'user'), related_name='employees')

    def __str__(self):
        """Return name of the company."""
        return self.name