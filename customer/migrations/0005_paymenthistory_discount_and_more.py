# Generated by Django 5.0.3 on 2024-04-10 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_alter_paymenthistory_due_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenthistory',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='paymenthistory',
            name='payment_status',
            field=models.CharField(choices=[('paid', 'Paid'), ('pending', 'Payment due later')], default='sdsd'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subscribedplan',
            name='payment_status',
            field=models.CharField(choices=[('paid', 'Paid'), ('pending', 'Payment due later')], default='pending', max_length=55, verbose_name='Payment Status'),
        ),
    ]
