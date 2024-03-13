# Generated by Django 5.0.2 on 2024-03-12 14:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
        ('yourhome', '0008_alter_property_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.country'),
        ),
    ]