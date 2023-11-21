# Generated by Django 3.2.21 on 2023-11-21 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bip', '0003_auto_20231121_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='behavior',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bip.behavior'),
        ),
        migrations.AlterField(
            model_name='case',
            name='frequency',
            field=models.PositiveIntegerField(blank=True, default=1, null=True, verbose_name='Frequency'),
        ),
    ]
