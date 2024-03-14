# Generated by Django 5.0.2 on 2024-03-14 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prospect', '0002_pointofcontactinfo_prospect'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pointofcontactinfo',
            old_name='pOC_name',
            new_name='contact_name',
        ),
        migrations.RenameField(
            model_name='prospectinfo',
            old_name='prospect_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='prospectinfo',
            old_name='street_loc',
            new_name='street',
        ),
        migrations.AlterField(
            model_name='prospectinfo',
            name='website',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Website'),
        ),
    ]