# Generated by Django 4.1 on 2024-03-05 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_rename_duration_months_customerplan_duration_in_months_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerinfo',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to='pictures'),
        ),
    ]
