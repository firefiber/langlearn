# Generated by Django 5.0 on 2024-05-04 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0003_alter_deckvisibility_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='visibility',
            field=models.ForeignKey(default='public', on_delete=models.SET('public'), to='learning.deckvisibility'),
        ),
    ]