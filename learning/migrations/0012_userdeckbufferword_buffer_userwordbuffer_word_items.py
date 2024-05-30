# Generated by Django 5.0 on 2024-05-29 15:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('languages', '0001_initial'),
        ('learning', '0011_userdeckbufferword_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdeckbufferword',
            name='buffer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='learning.userwordbuffer'),
        ),
        migrations.AddField(
            model_name='userwordbuffer',
            name='word_items',
            field=models.ManyToManyField(through='learning.UserDeckBufferWord', to='languages.word'),
        ),
    ]
