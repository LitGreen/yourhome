# Generated by Django 5.0.2 on 2024-04-17 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yourhome', '0006_property_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='avatar',
        ),
    ]