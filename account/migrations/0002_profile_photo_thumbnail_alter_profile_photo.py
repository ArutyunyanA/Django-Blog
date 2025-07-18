# Generated by Django 5.2 on 2025-05-04 16:04

import account.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='photo_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='profile_thumbnails/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/', validators=[account.validators.validate_image_format]),
        ),
    ]
