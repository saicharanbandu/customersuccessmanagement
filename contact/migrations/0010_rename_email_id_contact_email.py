# Generated by Django 5.0.2 on 2024-03-14 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0009_alter_contact_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='email_id',
            new_name='email',
        ),
    ]