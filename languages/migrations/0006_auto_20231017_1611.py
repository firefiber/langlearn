# Generated by Django 4.2.3 on 2023-10-17 14:11

from django.db import migrations, models
import hashlib


def populate_sentence_hash(apps, schema_editor):
    Sentence = apps.get_model('languages', 'Sentence')

    for sentence in Sentence.objects.filter(sentence_hash__isnull=True):
        sentence.sentence_hash = hashlib.sha256(sentence.sentence.encode()).hexdigest()
        sentence.save()


class Migration(migrations.Migration):

    dependencies = [
        ('languages', '0005_sentence_sentence_hash_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_sentence_hash)
    ]


