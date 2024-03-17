# Generated by Django 5.0.2 on 2024-03-17 18:38

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plan', '0001_initial'),
        ('prospect', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('legal_name', models.CharField(max_length=55, verbose_name='Legal Name')),
                ('profile_picture', models.ImageField(blank=True, upload_to='pictures')),
                ('display_name', models.CharField(max_length=55, verbose_name='Display Name')),
                ('short_name', models.CharField(max_length=50, verbose_name='Short Name or Abbreviation')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('prospect', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prospect.profile')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentHistory',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('payment_date', models.DateField()),
                ('due_date', models.DateField()),
                ('invoice_no', models.CharField(blank=True, max_length=25, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_payment', to='customer.profile')),
            ],
        ),
        migrations.CreateModel(
            name='SubscribedPlan',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('duration', models.IntegerField(default=0)),
                ('payment_status', models.CharField(choices=[('paid', 'Paid'), ('pending', 'Pending')], default='pending', max_length=55, verbose_name='Payment Status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_plan', to='customer.profile')),
                ('subscription_plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='plan.tariff')),
            ],
            options={
                'ordering': ('customer__legal_name',),
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=100)),
                ('designation', models.CharField(max_length=100)),
                ('mobile_no', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_user', to='customer.profile')),
            ],
        ),
        migrations.CreateModel(
            name='UserAppPermissions',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('module', models.CharField(max_length=25, null=True)),
                ('access_role', models.CharField(max_length=25, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_app_permissions_customer', to='customer.user')),
            ],
            options={
                'ordering': ('user__full_name',),
                'unique_together': {('user', 'module')},
            },
        ),
    ]
