# Generated by Django 4.2.1 on 2023-06-16 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0006_userlanguageproficiency_proficiency_weights'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlanguageproficiency',
            name='proficiency_level',
            field=models.FloatField(default=0.0),
        ),
    ]
