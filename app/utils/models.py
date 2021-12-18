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
        + created (DateTime): Store the datetime of the object was created.
        + updated (DateTime): Store the datetime of the object was updated.
    """

    created = models.DateTimeField(
        'created at', auto_now_add=True,
        help_text='Date time on which the was created.')

    updated = models.DateTimeField(
        'updated at', auto_now=True,
        help_text='Date time on which the was updated.')

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
        + email (EmailField): Store the email of the object.
        + phone_number (CharField): Store the phone_number of the object.
        + direction (CharField): Store the direction of the object.
        + country (CharField): Store the country of the object.
        + state (CharField): Store the state of the object.
        + city (CharField): Store the city of the object.
    """

    email = models.EmailField(
        'email address', unique=True,
        error_messages={'unique': 'A user with that email already exists.'})

    phone_regex = RegexValidator(
        regex=r"^\+1?\d{1,4}[ ]\d{10}$",
        message='Phone number must be entered in the format: +99 9999999999. Up to indicative + 10 digits allowed.')

    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)
    
    direction = models.CharField(max_length=25)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    class Meta:
        """Meta option."""
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created', '-updated']