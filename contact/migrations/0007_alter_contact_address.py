# Generated by Django 4.1 on 2024-03-08 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0006_alter_contact_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='address',
            field=models.CharField(max_length=255),
        ),
    ]