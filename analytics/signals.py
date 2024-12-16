from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.timezone import now
from habits.models import Habit
from analytics.models import HabitAnalytics, OverallAnalytics
from datetime import datetime

@receiver(post_save, sender=Habit)
def update_on_completion(sender, instance, **kwargs):
    if kwargs.get('task_marked', False):
        habit_analytics, created = HabitAnalytics.objects.get_or_create(habit=instance)
        habit_analytics.completed_days.append(now().date().strftime('%Y-%m-%d'))
        habit_analytics.last_updated = now()
        #check habit streak status
        if instance.streak:
            habit_analytics.highest_streak = max(habit_analytics.highest_streak, len(habit_analytics.completed_days))
        habit_analytics.save()

        # OverallAnalytics update logic
        overall_analytics,_ = OverallAnalytics.objects.get_or_create(user=instance.user)
        overall_analytics.total_completed_days += 1
        if instance.streak:
            overall_analytics.highest_streak = max(overall_analytics.highest_streak, habit_analytics.highest_streak)
        # updating activity log
        if str(now().date()) in overall_analytics.activity_log:
            overall_analytics.activity_log[str(now().date())] += 1
        else:
            overall_analytics.activity_log[str(now().date())] = 1
        overall_analytics.save()

        #debugging
        print('Task completion signal called!')

@receiver(post_save, sender=Habit)
def update_on_missed_days(sender, instance, **kwargs):
    if kwargs.get('task_missed', False):
        habit_analytics, _ = HabitAnalytics.objects.get_or_create(habit=instance)

        # log missed day
        habit_analytics.missed_days.append(instance.nxt_task_at.strftime('%Y-%m-%d'))
        habit_analytics.last_updated = now()
        habit_analytics.save()

        # OverallAnalytics update logic
        overall_analytics,_ = OverallAnalytics.objects.get_or_create(user=instance.user)
        overall_analytics.total_missed_days += 1
        overall_analytics.save()

        # debug
        print('Task missed signal called!')

@receiver(post_save, sender=Habit)
def progress_completed(sender, instance, **kwargs):
    if kwargs.get('habit_completed', False):
        overall_analytics,_ = OverallAnalytics.objects.get_or_create(user=instance.user)
        overall_analytics.total_habits_completed += 1
        overall_analytics.save()

# signal for initializing a habit analytics data
@receiver(post_save, sender=Habit)
def habit_initialized(sender, instance, **kwargs):
    if kwargs.get('habit_initialized', False):
        habit_analytics, created = HabitAnalytics.objects.get_or_create(habit=instance)
        habit_analytics.save()
        print('Habit Analytics data initialized')