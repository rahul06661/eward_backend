# Generated by Django 4.1.5 on 2023-03-23 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='family',
            name='relation',
            field=models.CharField(default=' ', max_length=100),
        ),
        migrations.AlterField(
            model_name='family',
            name='voter_id',
            field=models.CharField(max_length=20),
        ),
    ]