# Generated by Django 5.1.3 on 2024-12-07 18:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.CharField(choices=[('fitness', 'Fitness'), ('learning', 'Learning'), ('health', 'Health'), ('productivity', 'Productivity'), ('personal_development', 'Personal Development'), ('financial', 'Financial'), ('environmental', 'Environmental'), ('creative', 'Creative'), ('social', 'Social'), ('spiritual', 'Spiritual'), ('professional', 'Professional')], max_length=50)),
                ('duration', models.PositiveIntegerField(help_text='No. of repetitions.')),
                ('frequency', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('custom', 'Custom')], default='daily', max_length=20)),
                ('custom_days_gap', models.PositiveIntegerField(blank=True, help_text='In days. (Custom Frequency)', null=True)),
                ('count', models.IntegerField(default=0, max_length=10)),
                ('streak', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('nxt_task_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
