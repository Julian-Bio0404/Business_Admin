"""Employee models."""

# Django
from django.db import models

# Utils
from app.utils.models import BaseAppModel


class Employee(BaseAppModel):
    """
    Employee model.
    A employee is the table that holds the relationship between
    a user and a company.
    """

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE)

    def __str__(self):
        """Return username and company."""
        return f'{self.user} at {self.company}'