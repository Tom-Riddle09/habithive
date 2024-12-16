from django.db import models
from django.contrib.auth.models import User
from habits.models import Habit

class HabitAnalytics(models.Model):
    habit = models.OneToOneField(Habit, on_delete=models.CASCADE, related_name='analytics')
    completed_days = models.JSONField(default=list) # stores date of task completed days
    missed_days = models.JSONField(default=list) # stores date of task missed days.
    highest_streak = models.PositiveIntegerField(default=0) # highest streak obtained till now.
    last_updated = models.DateField(auto_now=True) # Notes modification date

    def __str__(self):
        return f'Analytics for {self.habit.name}' 
    
class OverallAnalytics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='overall_analytics')
    total_completed_days = models.PositiveIntegerField(default=0)
    total_habits_completed = models.PositiveIntegerField(default=0)
    total_missed_days = models.PositiveIntegerField(default=0)
    highest_streak = models.PositiveIntegerField(default=0)
    activity_log = models.JSONField(default=dict) # to store data related to users total activity day by day.

    def __str__(self):
        return f"Overall Analytics for {self.user.username}"
