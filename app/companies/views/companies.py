"""Companies views."""

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from app.companies.models import Company

# Serializer
from app.companies.serializers import CompanyModelSerializer, CreateCompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    Company Viewset.
    Handle the creation, updating, obtaining,
    listing and deletion of companies.
    """

    queryset = Company.objects.all()
    lookup_field = 'name'

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action == 'create':
            return CreateCompanySerializer
        return CompanyModelSerializer
