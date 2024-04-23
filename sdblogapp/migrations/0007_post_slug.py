# Generated by Django 5.0.1 on 2024-01-28 23:28

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sdblogapp', '0006_alter_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=None, editable=False, null=True, populate_from='title', unique=True),
        ),
    ]
