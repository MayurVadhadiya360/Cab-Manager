# Generated by Django 4.1 on 2023-11-09 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cab_management', '0002_rename_name_driver_username_driver_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='overall_rating',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3),
        ),
        migrations.AddField(
            model_name='ride',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
