# Generated by Django 5.0.3 on 2024-04-04 09:40

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('misc', '0002_alter_country_options_alter_state_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Prospect Name')),
                ('address', models.CharField(max_length=255, null=True, verbose_name='Street/Locality')),
                ('city', models.CharField(max_length=50, null=True, verbose_name='City/Town/Village')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Email ID')),
                ('website', models.CharField(blank=True, max_length=200, null=True, verbose_name='Website')),
                ('denomination', models.CharField(blank=True, max_length=50, null=True, verbose_name='Denomination')),
                ('congregation', models.IntegerField(blank=True, null=True, verbose_name='Congregation Size (Approx)')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='Remarks')),
                ('status', models.CharField(choices=[('initiated', 'First Call/Appointement Requested'), ('meeting scheduled', 'Meeting Scheduled'), ('awaiting', 'Awaiting Response'), ('accepted', 'Responded Yes'), ('rejected', 'Responded No')], max_length=55, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='misc.country')),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='prospect_manager', to=settings.AUTH_USER_MODEL)),
                ('state', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='misc.state')),
            ],
        ),
        migrations.CreateModel(
            name='PointOfContact',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Name')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Email ID')),
                ('mobile', models.CharField(blank=True, max_length=10, null=True, verbose_name='Mobile Number')),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('prospect', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prospect_poc', to='prospect.profile')),
            ],
        ),
        migrations.CreateModel(
            name='StatusHistory',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('initiated', 'First Call/Appointement Requested'), ('meeting scheduled', 'Meeting Scheduled'), ('awaiting', 'Awaiting Response'), ('accepted', 'Responded Yes'), ('rejected', 'Responded No')], max_length=55)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('prospect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prospect_history', to='prospect.profile')),
            ],
        ),
    ]
