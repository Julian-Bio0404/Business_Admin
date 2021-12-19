"""Companies URLs."""

#Django
from django.urls import path, include

# Django Rest Framework
from rest_framework.routers import DefaultRouter

# Views
from app.companies.views import CompanyViewSet, AccessPointViewSet, AccessHourViewSet


router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='companies')

router.register(
    r'companies/(?P<name>[-a-zA-Z0-0_]+)/access_points',
    AccessPointViewSet, basename='access_points')

router.register(
    r'companies/(?P<name>[-a-zA-Z0-0_]+)/access_hour',
    AccessHourViewSet, basename='access_hour')

urlpatterns = [
    path('', include(router.urls))
]