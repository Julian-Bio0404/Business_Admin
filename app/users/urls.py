"""Users URLs."""

#Django
from django.urls import path, include

# Django Rest Framework
from rest_framework.routers import DefaultRouter

#Views
from app.users.views import UserViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]