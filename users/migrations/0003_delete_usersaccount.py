# Generated by Django 5.1.3 on 2024-12-10 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_usersaccount_is_active'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UsersAccount',
        ),
    ]