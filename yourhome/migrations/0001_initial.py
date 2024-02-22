# Generated by Django 5.0.2 on 2024-02-22 19:06

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=250, verbose_name='Property Title')),
                ('slug', models.SlugField(allow_unicode=True, default='slug')),
                ('ref_code', models.CharField(blank=True, max_length=255, unique=True, verbose_name='Property Reference Code')),
                ('description', models.TextField(default='Add description here...', verbose_name='Description')),
                ('city', models.CharField(default='Nairobi', max_length=180, verbose_name='City')),
                ('postcode', models.CharField(default='140', max_length=100, verbose_name='Postcode')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Price')),
                ('plot_area', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Plot Area(m^2)')),
                ('total_floors', models.IntegerField(default=0, verbose_name='Number of floors')),
                ('bedrooms', models.IntegerField(default=1, verbose_name='Bedrooms')),
                ('bathrooms', models.DecimalField(decimal_places=2, default=1.0, max_digits=4, verbose_name='Bathrooms')),
                ('advert_type', models.CharField(choices=[('For Sale', 'For Sale'), ('For Rent', 'For Rent')], default='For Sale', max_length=50, verbose_name='Advert Type')),
                ('property_type', models.CharField(choices=[('House', 'House'), ('Apartment', 'Apartment'), ('Office', 'Office'), ('Warehouse', 'Warehouse'), ('Commercial', 'Commercial'), ('Other', 'Other')], default='Other', max_length=50, verbose_name='Property Type')),
                ('cover_photo', models.ImageField(blank=True, default='#', null=True, upload_to='', verbose_name='Main Photo')),
                ('photo1', models.ImageField(blank=True, default='', null=True, upload_to='')),
                ('photo2', models.ImageField(blank=True, default='', null=True, upload_to='')),
                ('photo3', models.ImageField(blank=True, default='', null=True, upload_to='')),
                ('photo4', models.ImageField(blank=True, default='', null=True, upload_to='')),
                ('published_status', models.BooleanField(default=False, verbose_name='Published Status')),
                ('views', models.IntegerField(default=0, verbose_name='Total Views')),
            ],
            options={
                'verbose_name': 'Property',
                'verbose_name_plural': 'Properties',
            },
        ),
    ]
