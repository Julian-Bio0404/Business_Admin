# Generated by Django 4.0 on 2021-12-18 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accesspoint',
            old_name='Geolocation',
            new_name='geolocation',
        ),
    ]
