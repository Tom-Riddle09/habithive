# Generated by Django 5.1.3 on 2024-12-10 16:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('habits', '0003_alter_habit_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HabitAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_days', models.JSONField(default=list)),
                ('missed_days', models.JSONField(default=list)),
                ('highest_streak', models.PositiveIntegerField(default=0)),
                ('last_updated', models.DateField(auto_now=True)),
                ('habit', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='analytics', to='habits.habit')),
            ],
        ),
        migrations.CreateModel(
            name='OverallAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_completed_days', models.PositiveIntegerField(default=0)),
                ('total_habits_completed', models.PositiveIntegerField(default=0)),
                ('highest_streak', models.PositiveIntegerField(default=0)),
                ('activity_log', models.JSONField(default=dict)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='overall_analytics', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
