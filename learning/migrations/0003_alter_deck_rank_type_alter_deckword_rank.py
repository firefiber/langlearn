# Generated by Django 5.0 on 2024-05-25 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='rank_type',
            field=models.CharField(choices=[('int', 'Integer'), ('float', 'Float')], default='float'),
        ),
        migrations.AlterField(
            model_name='deckword',
            name='rank',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]