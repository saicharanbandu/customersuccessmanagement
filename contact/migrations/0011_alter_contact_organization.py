# Generated by Django 5.0.2 on 2024-03-16 09:54

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0010_rename_email_id_contact_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='organization',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
