# Generated by Django 2.2 on 2021-12-28 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('image_id', models.IntegerField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(default=None, max_length=65536, unique=True)),
                ('image_path', models.ImageField(upload_to='user_img')),
                ('image_name', models.CharField(max_length=256)),
                ('image_size', models.CharField(default=None, max_length=256)),
                ('create_time', models.CharField(default='2021-12-28 05:17:41', max_length=256)),
                ('update_time', models.CharField(default='2021-12-28 05:17:41', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('register_id', models.IntegerField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(default=None, max_length=65536, unique=True)),
                ('username', models.CharField(max_length=256, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('gender', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=256, unique=True)),
                ('cellphone', models.IntegerField(default=20211228051741, null=True, unique=True)),
                ('fronted_email_code', models.CharField(default=None, max_length=256)),
                ('description', models.CharField(default=None, max_length=65536)),
                ('create_time', models.CharField(default='2021-12-28 05:17:41', max_length=256)),
                ('update_time', models.CharField(default='2021-12-28 05:17:41', max_length=256)),
            ],
        ),
    ]
