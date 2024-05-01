# Generated by Django 5.0 on 2024-05-01 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('languages', '0002_remove_word_frequency_rating_remove_word_pos'),
        ('learning', '0005_rename_priority_userworddeck_priority_rating_and_more'),
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='userworddeck',
            name='UserWordDeck_priority_range',
        ),
        migrations.AddConstraint(
            model_name='userworddeck',
            constraint=models.CheckConstraint(check=models.Q(('priority_rating__gte', 0.0), ('priority_rating__lte', 1.0)), name='UserWordDeck_priority_rating_range'),
        ),
    ]
