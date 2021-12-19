"""Access point views."""

# Django REST framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Models
from app.companies.models import AccessPoint, Company
from app.companies.models.access import AccessHour

# Serializers
from app.companies.serializers import (
    AccessHourModelSerializer,
    AccessPointModelSerializer,
    CreateAccessHourSerializer,
    CreateAccessPointSerializer
)


class AccessPointViewSet(viewsets.ModelViewSet):
    """
    Access Viewset.
    Handle the creation, updating, obtaining,
    listing and deletion of companies.
    """

    def dispatch(self, request, *args, **kwargs):
        """Verify that the company exists."""
        self.company = get_object_or_404(Company, name=kwargs['name'])
        return super(AccessPointViewSet, self).dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action == 'create':
            return CreateAccessPointSerializer
        return AccessPointModelSerializer

    def get_serializer_context(self):
        """Add company to serializer context."""
        context = super(AccessPointViewSet, self).get_serializer_context()
        if self.action == 'create':
            context['company'] = self.company
        return context

    def get_queryset(self):
        """Return access point of the company."""
        return AccessPoint.objects.filter(company=self.company)


class AccessHourViewSet(viewsets.ModelViewSet):
    """
    Access Hour viewset.
    Handle access permissions to access points.
    """

    def dispatch(self, request, *args, **kwargs):
        """Verify that the company exists."""
        self.company = get_object_or_404(Company, name=kwargs['name'])
        return super(AccessHourViewSet, self).dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action == 'create':
            return CreateAccessHourSerializer
        return AccessHourModelSerializer
    
    def get_serializer_context(self):
        """Add company to serializer context."""
        context = super(AccessHourViewSet, self).get_serializer_context()
        if self.action == 'create':
            context['company'] = self.company
        return context

    def get_queryset(self):
        """Return access hours of the company."""
        return AccessHour.objects.filter(access_point__company=self.company)