# Generated by Django 4.2.3 on 2023-11-09 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ComparisonMode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.CharField(choices=[('A', 'Mode A'), ('B', 'Mode B')], default='A', max_length=1)),
            ],
        ),
    ]
