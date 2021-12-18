"""Company serializers."""

# Django
from django.core.validators import RegexValidator

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Models
from app.companies.models import Company


class CompanyModelSerializer(serializers.ModelSerializer):
    """Company model serializer."""

    admin = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options."""
        model = Company
        fields = [
            'nit', 'name',
            'commercial_name', 'admin',
            'web_site', 'email',
            'phone_number', 'direction',
            'country', 'state', 'city'
        ]

        read_only_fields = [
            'nit', 'name',
            'admin'
        ]


class CreateCompanySerializer(serializers.Serializer):
    """Create Company Serializer."""

    # nit validator
    nit_regex = RegexValidator(
        regex=r"^\d{9,12}$", message='Nit number must has 9-12 digitis')

    nit = serializers.CharField(
        min_length=9, max_length=12,
        validators=[nit_regex, UniqueValidator(queryset=Company.objects.all())])
    
    name = serializers.CharField(
        min_length=3, max_length=80,
        validators=[UniqueValidator(queryset=Company.objects.all())])

    commercial_name = serializers.CharField(min_length=3, max_length=60)

    # Phone validator
    phone_regex = RegexValidator(
        regex=r"^\+1?\d{1,4}[ ]\d{10}$",
        message='Phone number must be entered in the format: +99 9999999999. Up to indicative + 10 digits allowed.')
    
    phone_number = serializers.CharField(
        min_length=13, max_length=17, validators=[phone_regex])
    
    web_site = serializers.URLField()

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=Company.objects.all())])
    
    direction = serializers.CharField(min_length=6, max_length=25)
    country = serializers.CharField(min_length=4, max_length=100)
    state = serializers.CharField(min_length=4, max_length=100)
    city = serializers.CharField(min_length=4, max_length=100)

    def create(self, data):
        """Handle company creation."""
        return Company.objects.create(**data)