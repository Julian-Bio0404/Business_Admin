"""Access serializers."""

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Models
from app.companies.models import AccessHour, AccessPoint, Employee


class AccessPointModelSerializer(serializers.ModelSerializer):
    """Access Point model serializer."""

    company = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options."""
        model = AccessPoint
        fields = [
            'name', 'company'
            'geolocation', 'active',
            'email', 'phone_number',
            'direction', 'country',
            'state', 'city'
        ]

        read_only_fields = [
            'company', 'geolocation'
        ]


class CreateAccessPointSerializer(serializers.Serializer):
    """Create Access Point serializer."""

    name = serializers.CharField(min_length=3, max_length=80)
    
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=AccessPoint.objects.all())])
    
    direction = serializers.CharField(min_length=6, max_length=25)
    country = serializers.CharField(min_length=4, max_length=100)
    state = serializers.CharField(min_length=4, max_length=100)
    city = serializers.CharField(min_length=4, max_length=100)

    active = serializers.BooleanField(required=False)

    def create(self, data):
        """Handle access point creation."""

        # No olvidar implementar geolocalización a partir de city
        # o direction, ya que este campo es requerido

        company = self.context['company']
        return AccessPoint.objects.create(**data, company=company)
    


class AccessHourModelSerializer(serializers.ModelSerializer):
    """Access Hour model serializer."""

    access_point = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options."""
        model = AccessHour
        fields = [
            'access_point', 'start'
            'finish', 'user', 'active'
        ]

        read_only_fields = ['access_point']


class CreateAccessHourSerializer(serializers.Serializer):
    """Create Hour serializer."""

    access_point = serializers.CharField(min_length=3, max_length=80)
    start = serializers.TimeField()
    finish = serializers.TimeField()
    active = serializers.BooleanField(required=False)
    employee = serializers.CharField(min_length=4, max_length=25)

    def validate_access_point(self, data):
        """Check that access point exists."""
        try:
            access_point = AccessPoint.objects.get(
                name=data, company=self.context['company'])
        except AccessPoint.DoesNotExist:
            raise serializers.ValidationError('Access point does not exists.')
        self.context['access_point'] = access_point
        return data

    def validate_employee(self, data):
        """Check that employee exists and belongs the company."""
        try:
            employee = Employee.objects.get(
                user=data, company=self.context['company'])
        except Employee.DoesNotExist:
            raise serializers.ValidationError('This user does not exists or is not a employee')
        self.context['employee'] = employee
        return data

    def validate(self, data):
        """check that the start time is before the end time."""
        if data['start'] >= data['finish']:
            raise serializers.ValidationError(
                'The start time be must before that the finish time.')
        return data

    def create(self, data):
        """Create a access hour."""
        company = self.context['company']
        access_point = self.context['access_point']
        employee = self.context['employee']

        data.pop('access_point')
        data.pop('employee')

        access_hour = AccessHour.objects.create(
            **data, company=company, access_point=access_point, user=employee)
        return access_hour
