# Generated by Django 5.0 on 2024-05-27 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0005_deck_is_ranked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deck',
            name='rank_type',
        ),
    ]