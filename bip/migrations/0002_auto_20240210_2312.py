# Generated by Django 3.2.21 on 2024-02-10 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bip', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataentry',
            name='assignedCaseManagerSlug',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='dataentry',
            name='assignedStudentSlug',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
