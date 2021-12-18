"""bussiness_admin URL Configuration."""

# Django
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('app.users.urls', 'users'), namespace='users')),
    path('', include(('app.companies.urls', 'companies'), namespace='companies')),
]
