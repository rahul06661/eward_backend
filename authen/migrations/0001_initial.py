# Generated by Django 4.1.5 on 2023-03-02 09:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False, unique=True)),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('age', models.CharField(max_length=3)),
                ('gender', models.CharField(max_length=3)),
                ('phone', models.CharField(max_length=12)),
                ('blood_group', models.CharField(max_length=3)),
                ('ward', models.CharField(max_length=3)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('email', models.EmailField(default=0, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('voter_id', models.CharField(max_length=20, unique=True)),
                ('job', models.CharField(max_length=20)),
                ('tax_payer', models.CharField(max_length=5)),
                ('age', models.CharField(max_length=3)),
                ('gender', models.CharField(max_length=3)),
                ('phone', models.CharField(max_length=12)),
                ('blood_group', models.CharField(max_length=3)),
                ('ward', models.CharField(max_length=3)),
                ('housenumber', models.CharField(max_length=3)),
                ('password', models.CharField(max_length=20)),
                ('date_of_birth', models.DateField(null=True)),
                ('qualification', models.CharField(max_length=100, null=True)),
                ('approval', models.BooleanField(default=False)),
                ('member_email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authen.member')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('utype', models.CharField(max_length=4)),
                ('session_token', models.CharField(default='0', max_length=10)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
    ]