# Generated by Django 4.1 on 2024-02-23 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_country_alter_customerinfo_zip_code_state_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerinfo',
            name='zip_code',
            field=models.IntegerField(verbose_name='Zip/Postal Code'),
        ),
    ]
