# Generated by Django 5.0.3 on 2024-04-08 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prospect', '0002_alter_profile_status_alter_statushistory_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pointofcontact',
            name='mobile',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Mobile Number'),
        ),
    ]
