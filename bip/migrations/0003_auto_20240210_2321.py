# Generated by Django 3.2.21 on 2024-02-10 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bip', '0002_auto_20240210_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='bio',
            field=models.CharField(blank=True, max_length=45, null=True, verbose_name='Occupation'),
        ),
        migrations.AlterField(
            model_name='dataentry',
            name='assignedCaseManagerSlug',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name='dataentry',
            name='assignedStudentSlug',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
    ]
