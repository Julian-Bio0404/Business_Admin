# Generated by Django 4.0 on 2021-12-19 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0004_accesshour_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesspoint',
            name='geolocation',
            field=models.CharField(max_length=30),
        ),
    ]
