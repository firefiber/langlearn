# Generated by Django 4.2.1 on 2023-06-06 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('languages', '0002_sentencetype_sentence_words_sentence_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentence',
            name='theme',
            field=models.CharField(default='general', max_length=100),
        ),
    ]
