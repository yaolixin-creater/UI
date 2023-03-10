# Generated by Django 2.2 on 2022-03-15 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctc_backend_manage', '0003_auto_20211228_0832'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='status_cd',
        ),
        migrations.AlterField(
            model_name='case',
            name='create_time',
            field=models.CharField(default='2022-03-15 22:42:07', max_length=256),
        ),
        migrations.AlterField(
            model_name='case',
            name='update_time',
            field=models.CharField(default='2022-03-15 22:42:07', max_length=256),
        ),
        migrations.AlterField(
            model_name='envmanagement',
            name='create_time',
            field=models.CharField(default='2022-03-15 22:42:07', max_length=256),
        ),
        migrations.AlterField(
            model_name='envmanagement',
            name='update_time',
            field=models.CharField(default='2022-03-15 22:42:07', max_length=256),
        ),
        migrations.AlterField(
            model_name='groupmanagement',
            name='create_time',
            field=models.CharField(default='2022-03-15 22:42:07', max_length=256),
        ),
        migrations.AlterField(
            model_name='groupmanagement',
            name='update_time',
            field=models.CharField(default='2022-03-15 22:42:07', max_length=256),
        ),
        migrations.AlterField(
            model_name='item',
            name='create_time',
            field=models.CharField(default='2022-03-15 22:42:07', max_length=256),
        ),
        migrations.AlterField(
            model_name='item',
            name='update_time',
            field=models.CharField(default='2022-03-15 22:42:07', max_length=256),
        ),
        migrations.AlterField(
            model_name='loginresult',
            name='create_time',
            field=models.CharField(default='2022-03-15 22:42:07', max_length=256),
        ),
        migrations.AlterField(
            model_name='loginresult',
            name='update_time',
            field=models.CharField(default='2022-03-15 22:42:07', max_length=256),
        ),
        migrations.AlterField(
            model_name='reporter',
            name='create_time',
            field=models.CharField(default='2022-03-15 22:42:07', max_length=256),
        ),
        migrations.AlterField(
            model_name='reporter',
            name='update_time',
            field=models.CharField(default='2022-03-15 22:42:07', max_length=256),
        ),
        migrations.AlterField(
            model_name='step',
            name='create_time',
            field=models.CharField(default='2022-03-15 22:42:07', max_length=256),
        ),
        migrations.AlterField(
            model_name='step',
            name='update_time',
            field=models.CharField(default='2022-03-15 22:42:07', max_length=256),
        ),
    ]
