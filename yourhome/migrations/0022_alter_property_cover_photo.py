# Generated by Django 5.0.2 on 2024-04-15 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yourhome', '0021_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='cover_photo',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Main Photo'),
        ),
    ]
