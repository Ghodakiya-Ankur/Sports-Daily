# Generated by Django 5.0.1 on 2024-03-05 03:02

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sdmember', '0004_otps_delete_otp'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OTPS',
            new_name='OTP',
        ),
    ]