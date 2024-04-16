# Generated by Django 5.0.3 on 2024-04-04 09:40

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
            ],
            options={
                'ordering': ('user__full_name',),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('profile_picture', models.ImageField(blank=True, upload_to='pictures')),
                ('legal_name', models.CharField(max_length=55, verbose_name='Legal Name')),
                ('display_name', models.CharField(max_length=55, verbose_name='Display Name')),
                ('short_name', models.CharField(max_length=50, verbose_name='Short Name or Abbreviation')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='customer_manager', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
