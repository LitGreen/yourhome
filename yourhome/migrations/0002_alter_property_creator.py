# Generated by Django 5.0.2 on 2024-04-15 16:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yourhome', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='creator',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='yourhome.user', verbose_name='Listed by'),
        ),
    ]
