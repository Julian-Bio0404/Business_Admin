"""Employees serializers."""

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Models
from app.companies.models import Employee
from app.users.models import User

# Taskapp
from taskapp.tasks.users import send_invitation_email


class InviteEmployee(serializers.Serializer):
    """
    Invite Employee.
    It is util for invite a employee to register in the app.
    """

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    
    def create(self, data):
        """Handle the sending of invitations to an email."""
        company = self.context['company']
        send_invitation_email.delay(
            email=data['email'], company_name=company.name)
        return data['email']


class EmployeeModelSerializer(serializers.ModelSerializer):
    """Employee Model serializer."""
    
    user = serializers.StringRelatedField(read_only=True)
    joined_at = serializers.DateTimeField(source='created', read_only=True)

    class Meta:
        """Meta options."""
        model = Employee
        fields = ['user', 'joined_at']
        read_only_fields = ['user', 'joined_at']
