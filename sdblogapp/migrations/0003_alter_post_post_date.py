# Generated by Django 5.0.1 on 2024-01-28 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdblogapp', '0002_post_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
