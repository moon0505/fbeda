# Generated by Django 3.2.21 on 2023-11-08 21:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bip', '0003_auto_20230812_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='casemanager',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='bip.casemanager'),
        ),
    ]
