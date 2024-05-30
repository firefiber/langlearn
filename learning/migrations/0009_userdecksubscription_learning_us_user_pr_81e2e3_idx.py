# Generated by Django 5.0 on 2024-05-29 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0008_alter_deckword_unique_together'),
        ('user_management', '0002_alter_userlearninglanguage_proficiency_level'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='userdecksubscription',
            index=models.Index(fields=['user_profile', 'deck'], name='learning_us_user_pr_81e2e3_idx'),
        ),
    ]