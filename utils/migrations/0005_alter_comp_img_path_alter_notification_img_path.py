# Generated by Django 4.1.5 on 2023-04-02 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0004_alter_comp_img_path_alter_notification_img_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comp',
            name='img_path',
            field=models.ImageField(null=True, upload_to='media'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='img_path',
            field=models.ImageField(null=True, upload_to='media'),
        ),
    ]
