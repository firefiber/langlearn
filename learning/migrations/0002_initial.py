# Generated by Django 5.0 on 2024-05-25 09:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('languages', '0001_initial'),
        ('learning', '0001_initial'),
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user_management.userprofile'),
        ),
        migrations.AddField(
            model_name='deck',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='languages.language'),
        ),
        migrations.AddField(
            model_name='deckword',
            name='deck',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning.deck'),
        ),
        migrations.AddField(
            model_name='deckword',
            name='word_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='languages.word'),
        ),
        migrations.AddField(
            model_name='deck',
            name='word_items',
            field=models.ManyToManyField(through='learning.DeckWord', to='languages.word'),
        ),
        migrations.AddField(
            model_name='userdecksubscription',
            name='deck',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning.deck'),
        ),
        migrations.AddField(
            model_name='userdecksubscription',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.userprofile'),
        ),
        migrations.AddField(
            model_name='userwordbank',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='languages.language'),
        ),
        migrations.AddField(
            model_name='userwordbank',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.userprofile'),
        ),
        migrations.AddField(
            model_name='userwordbank',
            name='word_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='languages.word'),
        ),
        migrations.AddField(
            model_name='userwordbuffer',
            name='deck_source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='learning.deck'),
        ),
        migrations.AddField(
            model_name='userwordbuffer',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='languages.language'),
        ),
        migrations.AddField(
            model_name='userwordbuffer',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.userprofile'),
        ),
        migrations.AddField(
            model_name='userwordbuffer',
            name='word_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='languages.word'),
        ),
        migrations.AddIndex(
            model_name='deck',
            index=models.Index(fields=['name', 'language'], name='learning_de_name_855535_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='deck',
            unique_together={('name', 'language', 'created_by')},
        ),
        migrations.AlterUniqueTogether(
            name='userdecksubscription',
            unique_together={('user_profile', 'deck', 'is_active')},
        ),
        migrations.AddIndex(
            model_name='userwordbank',
            index=models.Index(fields=['user_profile', 'word_item'], name='learning_us_user_pr_9a0e69_idx'),
        ),
        migrations.AddIndex(
            model_name='userwordbuffer',
            index=models.Index(fields=['user_profile', 'deck_source'], name='learning_us_user_pr_446ce2_idx'),
        ),
        migrations.AddIndex(
            model_name='userwordbuffer',
            index=models.Index(fields=['user_profile', 'priority'], name='learning_us_user_pr_fabb82_idx'),
        ),
        migrations.AddConstraint(
            model_name='userwordbuffer',
            constraint=models.CheckConstraint(check=models.Q(('proficiency__gte', 0.0), ('proficiency__lte', 1.0)), name='UserWordBuffer_proficiency_range'),
        ),
    ]