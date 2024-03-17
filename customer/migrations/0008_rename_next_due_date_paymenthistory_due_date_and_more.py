# Generated by Django 5.0.2 on 2024-03-17 17:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_alter_user_designation_alter_user_email_and_more'),
        ('plan', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paymenthistory',
            old_name='next_due_date',
            new_name='due_date',
        ),
        migrations.AlterField(
            model_name='subscribedplan',
            name='customer',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_plan', to='customer.profile'),
        ),
        migrations.AlterField(
            model_name='subscribedplan',
            name='subscription_plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='plan.tariff'),
        ),
    ]
