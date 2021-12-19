"""Companies tasks."""

from __future__ import absolute_import, unicode_literals

# Django
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Celery
from taskapp.celery import app

# Models
from app.users.models import User


@app.task
def admin_notification_email(admin_pk: int, user_pk: int):
    """Send an email notification to a company admin."""
    admin = User.objects.get(pk=admin_pk)
    user = User.objects.get(pk=user_pk)

    subject = 'Notification of failed access'
    from_email = 'Business-Admin <businessadmin.com>'
    content = render_to_string(
        'companies/notification.html', {'admin': admin, 'user': user})
    msg = EmailMultiAlternatives(subject, content, from_email, [admin.email])
    msg.attach_alternative(content, 'text/html')
    msg.send()
