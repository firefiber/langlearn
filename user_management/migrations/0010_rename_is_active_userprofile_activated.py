# Generated by Django 5.0 on 2023-12-07 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0009_userprofile_is_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='is_active',
            new_name='activated',
        ),
    ]