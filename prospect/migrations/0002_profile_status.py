# Generated by Django 5.0.2 on 2024-03-25 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prospect', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='status',
            field=models.CharField(choices=[('first_call', 'First Call'), ('meeting scheduled', 'Meeting Scheduled'), ('waiting', 'Awaiting Response'), ('accepted', 'Responded Yes'), ('rejected', 'Responded No')], default='pending', max_length=55, verbose_name='Payment Status'),
        ),
    ]