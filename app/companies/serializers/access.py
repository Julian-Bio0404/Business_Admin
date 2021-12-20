"""Access serializers."""

# Utilities
from datetime import datetime

# Django REST Framework
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Models
from app.companies.models import AccessHour, AccessPoint, Employee
from app.users.models.users import User

# Utils
from app.utils.services import api_maps


class AccessPointModelSerializer(serializers.ModelSerializer):
    """Access Point model serializer."""

    company = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options."""
        model = AccessPoint
        fields = [
            'name', 'company',
            'geolocation', 'active',
            'email', 'phone_number',
            'direction', 'country',
            'state', 'city'
        ]

        read_only_fields = [
            'company', 'country',
            'state', 'city'
        ]
    
    def update(self, instance, validated_data):
        """
        Update access point, if geolocation needs to be
        updated, country, state and city will also be updated.
        """
        geolocation = validated_data.get('geolocation', None)
        if geolocation:
            geolocation = api_maps(validated_data['geolocation'])
            if geolocation:
                country = geolocation['country']
                state = geolocation['state']
                city = geolocation['city']

                instance.country = country
                instance.state = state
                instance.city = city
        return super().update(instance, validated_data)


class CreateAccessPointSerializer(serializers.Serializer):
    """Create Access Point serializer."""

    name = serializers.CharField(min_length=3, max_length=80)
    
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=AccessPoint.objects.all())])

    # Geolocation validation
    geo_regex = RegexValidator(
        regex=r"^(-?\d+(\.\d+)?),*(-?\d+(\.\d+)?)$",
        message='Geolocation must be entered in the format: lat,lon')

    geolocation = serializers.CharField(
        validators=[geo_regex], min_length=6, max_length=30)

    direction = serializers.CharField(min_length=6, max_length=25)
    active = serializers.BooleanField(required=False)

    def create(self, data):
        """Handle access point creation."""
        geolocation = api_maps(data['geolocation'])
        if geolocation:
            country = geolocation['country']
            state = geolocation['state']
            city = geolocation['city']
        company = self.context['company']
        access_point = AccessPoint.objects.create(
            **data, company=company,
            country=country, state=state, city=city)
        return access_point


class AccessHourModelSerializer(serializers.ModelSerializer):
    """Access Hour model serializer."""

    access_point = serializers.StringRelatedField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options."""
        model = AccessHour
        fields = [
            'access_point', 'start',
            'finish', 'user', 'active'
        ]

        read_only_fields = ['access_point', 'user']


class CreateAccessHourSerializer(serializers.Serializer):
    """Create Hour serializer."""

    access_point = serializers.CharField(min_length=3, max_length=80)
    start = serializers.TimeField()
    finish = serializers.TimeField()
    active = serializers.BooleanField(required=False)
    user = serializers.CharField(min_length=4, max_length=25)

    def validate_access_point(self, data):
        """Check that access point exists."""
        try:
            access_point = AccessPoint.objects.get(
                name=data, company=self.context['company'])
        except AccessPoint.DoesNotExist:
            raise serializers.ValidationError('Access point does not exists.')
        self.context['access_point'] = access_point
        return data

    def validate_user(self, data):
        """Check that employee exists and belongs the company."""
        try:
            user = User.objects.get(username=data)
        except User.DoesNotExist:
            raise serializers.ValidationError('This user does not exists.')
        
        employee = Employee.objects.filter(
            user=user, company=self.context['company'])

        if employee.exists() != True:
            raise serializers.ValidationError('This user is not an employee in this company.')
        self.context['employee'] = user
        return data

    def validate(self, data):
        """check that the start time is before the end time."""
        if data['start'] >= data['finish']:
            raise serializers.ValidationError(
                'The start time be must before that the finish time.')
        return data

    def create(self, data):
        """Create a access hour."""
        access_point = self.context['access_point']
        user = self.context['employee']
        data.pop('access_point')
        data.pop('user')

        access_hour = AccessHour.objects.create(
            **data, access_point=access_point, user=user)
        return access_hour


class VerifyAccessSerializer(serializers.Serializer):
    """Verify Access serializer."""

    # Geolocation validation
    geo_regex = RegexValidator(
        regex=r"^(-?\d+(\.\d+)?),*(-?\d+(\.\d+)?)$",
        message='Geolocation must be entered in the format: lat,lon')

    geolocation = serializers.CharField(
        validators=[geo_regex], min_length=6, max_length=30)
    
    def validate(self, data):
        """Verify access permission."""
        access_point = self.context['access_point']
        user = self.context['user']

        now = datetime.now().time()
        access_hour = AccessHour.objects.filter(
            access_point=access_point,
            access_point__geolocation=data['geolocation'],
            user=user, active=True,
            start__lte=now, finish__gt=now,
        )

        if access_hour.exists():
            self.context['access'] = True
        else:
            self.context['access'] = False
        return data
    
    def save(self, **kwargs):
        return self.context['access']