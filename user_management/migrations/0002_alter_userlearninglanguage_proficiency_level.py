# Generated by Django 5.0 on 2024-05-25 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlearninglanguage',
            name='proficiency_level',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3),
        ),
    ]