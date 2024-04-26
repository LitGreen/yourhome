# Generated by Django 5.0.2 on 2024-04-25 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yourhome', '0011_alter_avatar_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='cover_photo',
            field=models.ImageField(blank=True, null=True, upload_to='static/images/properties/', verbose_name='Main Photo'),
        ),
        migrations.AlterField(
            model_name='property',
            name='photo1',
            field=models.ImageField(blank=True, null=True, upload_to='static/images/properties/', verbose_name='Photo 1'),
        ),
        migrations.AlterField(
            model_name='property',
            name='photo2',
            field=models.ImageField(blank=True, null=True, upload_to='static/images/properties/', verbose_name='Photo 2'),
        ),
        migrations.AlterField(
            model_name='property',
            name='photo3',
            field=models.ImageField(blank=True, null=True, upload_to='static/images/properties/', verbose_name='Photo 3'),
        ),
        migrations.AlterField(
            model_name='property',
            name='photo4',
            field=models.ImageField(blank=True, null=True, upload_to='static/images/properties/', verbose_name='Photo 4'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]