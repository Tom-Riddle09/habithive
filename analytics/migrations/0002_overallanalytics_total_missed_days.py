# Generated by Django 5.1.3 on 2024-12-11 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='overallanalytics',
            name='total_missed_days',
            field=models.PositiveIntegerField(default=0),
        ),
    ]