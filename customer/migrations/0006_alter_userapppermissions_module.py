# Generated by Django 5.0.3 on 2024-04-11 07:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_paymenthistory_discount_and_more'),
        ('misc', '0003_appmodule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userapppermissions',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='misc.appmodule'),
        ),
    ]
