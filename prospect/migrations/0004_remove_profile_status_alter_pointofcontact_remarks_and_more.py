# Generated by Django 4.1 on 2024-03-26 08:58

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('prospect', '0003_alter_profile_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='status',
        ),
        migrations.AlterField(
            model_name='pointofcontact',
            name='remarks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='StatusHistory',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('initiated', 'First Call'), ('meeting scheduled', 'Meeting Scheduled'), ('awaiting', 'Awaiting Response'), ('accepted', 'Responded Yes'), ('rejected', 'Responded No')], max_length=55, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('prospect', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prospect_history', to='prospect.profile')),
            ],
        ),
    ]
