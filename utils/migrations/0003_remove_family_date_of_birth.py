# Generated by Django 4.1.5 on 2023-03-27 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0002_family_relation_alter_family_voter_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='family',
            name='date_of_birth',
        ),
    ]
