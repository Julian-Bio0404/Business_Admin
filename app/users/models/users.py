"""User models."""

# Django
from django.contrib.auth.models import AbstractUser
from django.db import models

# Utils
from app.utils.models import AppModel


class User(AppModel, AbstractUser):
    """
    User model.
    Extend from Django's Abstract User and add some extra fields.
    """

    company = models.ForeignKey(
        'companies.Company', on_delete=models.CASCADE,
        help_text='company to which the user belongs')

    verified = models.BooleanField(
        default=False, help_text='Set to true when the user have verified its email add')

    # Username configuration
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        """Return username."""
        return self.username

    def get_short_name(self):
        """Return username."""
        return self.username