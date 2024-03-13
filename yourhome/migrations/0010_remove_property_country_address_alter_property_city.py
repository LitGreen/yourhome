# Generated by Django 5.0.2 on 2024-03-12 18:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    ependencies = [
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
        ('yourhome', '0009_property_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.city')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.country')),
            ],
        ),
        migrations.AlterField(
            model_name='property',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='yourhome.address'),
        ),
    ]