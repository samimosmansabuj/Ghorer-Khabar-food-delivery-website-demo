# Generated by Django 5.0.1 on 2024-01-16 18:18

import django.contrib.auth.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Custom_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=100, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator])),
                ('email', models.EmailField(max_length=150)),
                ('phone_number', models.CharField(max_length=14)),
                ('user_type', models.CharField(blank=True, choices=[('Admin', 'Admin'), ('Staff', 'Staff'), ('Normal User', 'Normal User'), ('Merchant', 'Merchant')], max_length=20, null=True)),
                ('joined_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_varified', models.BooleanField(default=False)),
                ('auth_token', models.CharField(blank=True, max_length=500, null=True)),
                ('otp_token', models.CharField(blank=True, max_length=6, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Merchant_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('company_name', models.CharField(blank=True, max_length=200, null=True)),
                ('company_logo', models.ImageField(blank=True, null=True, upload_to='company/logo/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Normal_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='regular_user/picture/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='regular_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
