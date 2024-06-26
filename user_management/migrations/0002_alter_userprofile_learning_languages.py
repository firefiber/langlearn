# Generated by Django 4.2.1 on 2023-05-19 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('languages', '0001_initial'),
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='learning_languages',
            field=models.ManyToManyField(related_name='learning_users', through='user_management.UserLanguageProficiency', to='languages.language'),
        ),
    ]
