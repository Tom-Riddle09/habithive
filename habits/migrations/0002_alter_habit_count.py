# Generated by Django 5.1.3 on 2024-12-07 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
