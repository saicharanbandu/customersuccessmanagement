# Generated by Django 5.0.2 on 2024-03-16 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prospect', '0007_profile_remarks_alter_pointofcontact_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='congregation',
            field=models.IntegerField(blank=True, null=True, verbose_name='Congregation Size (Approx)'),
        ),
    ]
