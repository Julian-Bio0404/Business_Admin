"""Django abstract models utilities."""

# Django
from django.core.validators import RegexValidator
from django.db import models


class BaseAppModel(models.Model):
    """
    Base App Model.
    BaseAppModel acts as an abstract base class from which every
    other model in the project will inherit. This class provides
    every table with the following atribute:
        + created (DateTime): Store the datetime the object was created.
    """

    created = models.DateTimeField(
        'created at', auto_now_add=True,
        help_text='Date time on which the was created.')

    class Meta:
        """Meta option."""
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created']


class AppModel(BaseAppModel):
    """
    App Model.
    AppModel acts as an abstract base class inherits from
    BaseAppModel. Extend your models of this class to add 
    the following field:
        + updated (DateTime): Store the datetime the object was updated.
    """

    updated = models.DateTimeField(
        'updated at', auto_now=True,
        help_text='Date time on which the was updated.')

    email = models.EmailField(
        'email address', unique=True,
        error_messages={'unique': 'A user with that email already exists.'})

    phone_regex = RegexValidator(
        regex=r"^\+1?\d{1,4}[ ]\d{10}$",
        message='Phone number must be entered in the format: +99 9999999999. Up to indicative + 10 digits allowed.')

    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)

    class Meta:
        """Meta option."""
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created', '-updated']