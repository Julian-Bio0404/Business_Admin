"""Access models."""

# Django
from django.db import models

# Utils
from app.utils.models import AppModel, BaseAppModel


class AccessPoint(AppModel):
    """
    Access Point model.
    Saves data from a headquarters of a company.
    """

    name = models.CharField(max_length=80)
    company = models.ForeignKey(
        'companies.Company', on_delete=models.CASCADE, help_text='company to which the user belongs')

    geolocation = models.CharField(max_length=15)
    active = models.BooleanField(default=False)

    def __str__(self):
        """Return name and company."""
        return f'{self.company}:{self.name}'


class AccessHour(BaseAppModel):
    """
    Access Hour model.
    save the access times of a headquarters
    """

    access_point = models.ForeignKey('companies.AccessPoint', on_delete=models.CASCADE)
    start = models.TimeField(help_text='Start time')
    finish = models.TimeField(help_text='Finish time')
    active = models.BooleanField(default=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        """Return name and company."""
        return f'{self.start}-{self.finish}'
