# Generated by Django 3.2.21 on 2024-06-08 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bip', '0003_auto_20240210_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anticedent',
            name='anticedentincident',
            field=models.CharField(default='Test', max_length=50, verbose_name='Antecedent'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='consequence',
            name='behaviorconsequence',
            field=models.CharField(default='TestBeh', max_length=30, verbose_name='Consequence'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='function',
            name='behaviorfunction',
            field=models.CharField(default='TestBehFunc', max_length=30, verbose_name='Function'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='studentname',
            field=models.CharField(default='TestName', max_length=30, verbose_name='Name'),
            preserve_default=False,
        ),
    ]
