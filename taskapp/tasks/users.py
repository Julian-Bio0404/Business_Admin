"""Users tasks."""

from __future__ import absolute_import, unicode_literals

# Utilities
from datetime import timedelta
import jwt

# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Celery
from taskapp.celery import app

# Models
from app.users.models import User


def token_generation(user: User, type: str) -> str:
    """Create JWT token."""
    exp_date = timezone.now() + timedelta(days=2)
    payload = {
        'user': user.username,
        'exp': int(exp_date.timestamp()),
        'type': type
        }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


# Asynch task
@app.task
def send_confirmation_email(user_pk: int):
    """Send account verification link to given user."""
    user = User.objects.get(pk=user_pk)
    token = token_generation(user, type='email_confirmation')
    subject = f'Welcome @{user.get_full_name()}! Verify your account'
    from_email = 'Business-Admin <businessadmin.com>'
    content = render_to_string(
        'users/account_verification.html', {'token': token, 'user': user})
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, 'text/html')
    msg.send()


# Asynch task
@app.task
def send_restore_password_email(user_pk: int):
    """Send restore password link to given user."""
    user = User.objects.get(pk=user_pk)
    token = token_generation(user, type='restore_password')
    subject = 'Update your password'
    from_email = 'Business-Admin <businessadmin.com>'
    content = render_to_string(
        'users/restore_password.html', {'token': token, 'user': user})
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, 'text/html')
    msg.send()