# Generated by Django 5.0.1 on 2024-01-28 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdblogapp', '0003_alter_post_post_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(default='blog', max_length=255),
        ),
    ]