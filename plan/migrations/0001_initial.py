# Generated by Django 5.0.2 on 2024-03-17 18:38

import django.contrib.postgres.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppModule',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('permissions', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=10), blank=True, null=True, size=4)),
                ('precedance', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('modules', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), null=True, size=30)),
                ('lower_limit', models.IntegerField()),
                ('upper_limit', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
