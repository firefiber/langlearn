# Generated by Django 4.2.3 on 2023-11-05 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('languages', '0011_alter_sentence_translation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentence',
            name='translation',
            field=models.ManyToManyField(blank=True, related_name='translated_sentences', to='languages.sentence'),
        ),
    ]
