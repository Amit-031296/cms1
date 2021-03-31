# Generated by Django 3.1.7 on 2021-03-20 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CMSAuthor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=60, unique=True)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('user_password', models.CharField(max_length=50)),
                ('user_firstname', models.CharField(max_length=50)),
                ('user_lastname', models.CharField(max_length=50)),
                ('user_phone_number', models.CharField(max_length=17)),
                ('user_address', models.TextField(blank=True, default='')),
                ('user_city', models.CharField(blank=True, default='', max_length=50)),
                ('user_state', models.CharField(blank=True, default='', max_length=50)),
                ('user_country', models.CharField(blank=True, default='', max_length=50)),
                ('user_pincode', models.CharField(max_length=6)),
                ('user_role', models.CharField(default='Author', max_length=6)),
            ],
        ),
    ]
