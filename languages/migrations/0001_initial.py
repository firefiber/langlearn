# Generated by Django 5.0 on 2024-05-25 09:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=3)),
                ('category', models.CharField(choices=[('L', 'Learning'), ('N', 'Native'), ('B', 'Both')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='SentenceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='languages.language')),
            ],
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentence', models.TextField()),
                ('sentence_hash', models.CharField(max_length=64, unique=True)),
                ('complexity_rating', models.FloatField(blank=True, null=True)),
                ('theme', models.CharField(blank=True, default='general', max_length=100)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='languages.language')),
                ('translation', models.ManyToManyField(blank=True, related_name='translated_sentences', to='languages.sentence')),
                ('type', models.ManyToManyField(blank=True, to='languages.sentencetype')),
                ('words', models.ManyToManyField(blank=True, to='languages.word')),
            ],
        ),
        migrations.CreateModel(
            name='WordInSentence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='languages.sentence')),
                ('word_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='languages.word')),
            ],
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='translation_sources', to='languages.language')),
                ('source_sentence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations_from', to='languages.sentence')),
                ('translated_language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='translated_languages', to='languages.language')),
                ('translated_sentence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations_to', to='languages.sentence')),
            ],
            options={
                'unique_together': {('source_sentence', 'translated_sentence')},
            },
        ),
        migrations.AddIndex(
            model_name='word',
            index=models.Index(fields=['language', 'value'], name='languages_w_languag_08e217_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='word',
            unique_together={('language', 'value')},
        ),
        migrations.AddIndex(
            model_name='wordinsentence',
            index=models.Index(fields=['word_item', 'sentence'], name='languages_w_word_it_4ab624_idx'),
        ),
    ]
