# Generated by Django 4.1 on 2024-03-06 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_merge_20240305_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerinfo',
            name='legal_name',
            field=models.CharField(max_length=55, verbose_name='Legal Name'),
        ),
    ]
