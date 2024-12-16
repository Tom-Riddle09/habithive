from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import Habit
from analytics.models import OverallAnalytics
from .forms import HabitForm
from datetime import timedelta
from django.db import models
import random
from django.db.models.signals import post_save


# message to be shown when user completes a task
motivational_messages = [
    "Keep going, you're doing great!",
    "Believe in yourself and all that you are!",
    "Small steps every day lead to big changes.",
    "Consistency is the key to success.",
    "Your future self will thank you for the effort you put in today.",
    "Every habit you create brings you closer to your goals.",
    "Don't watch the clock; do what it does. Keep going.",
    "Your only limit is you. Push past it!",
    "Celebrate every small victory along the way.",
    "Make today so awesome that yesterday gets jealous.",
    "You are capable of amazing things.",
    "Start where you are. Use what you have. Do what you can.",
    "Success doesn’t come from what you do occasionally; it comes from what you do consistently.",
    "Dream big. Start small. Act now.",
    "Progress is progress, no matter how small.",
    "Stay positive, work hard, make it happen.",
    "The secret of getting ahead is getting started.",
    "You don’t have to be perfect to be amazing.",
    "Motivation gets you started, but habit keeps you going.",
    "Don’t give up. Great things take time."
]

@login_required
def dashboard(request):
    user_habits = Habit.objects.filter(user=request.user, is_active=True)
    # highest streak implementation
    analytics = get_object_or_404(OverallAnalytics,user=request.user)
    highest_streak = analytics.highest_streak
    remainder_habits = []
    notification = []
    # check remainder and streak updates
    for habit in user_habits:
        if habit.nxt_task_at.date() == habit.created_at.date():
            habit.set_remainder()
            print(f'Next date updated for habit {habit.name}')
        if habit.nxt_task_at.date() == now().date():
            remainder_habits.append(f'Remainder: Do not forget to complete today`s task "{habit}".')
        elif habit.nxt_task_at.date() < now().date() and habit.streak:
            remainder_habits.append(f"You have lost your streak of habit '{habit}' :(")
            habit.streak = False
            habit.save()
            # manual trigger for analytics:signals
            post_save.send(sender=Habit, instance=habit, task_missed=True)

            habit.set_remainder()

    # progress calculation
    progress_data = []
    for habit in user_habits:
        progress = habit.calculate_progress(habit.count)
        progress_data.append({
            'habit':habit,
            'progress':progress
        })
        # notification when progress is 100%
        if progress == 100:
            notification.append(f"Congratulations! You've acheived your goal for {habit.name}!")
            habit.is_active = False
            habit.save()
            post_save.send(sender=Habit, instance=habit, habit_completed=True)

    # data for dashboard sections
    category_data = Habit.objects.filter(user=request.user, is_active=True).values('category').annotate(count=models.Count('category'))
    category_labels = [entry['category'].capitalize() for entry in category_data]
    category_values = [int(entry['count']) for entry in category_data]


    context = {
        'reminder_habits':remainder_habits,
        'notification':notification,
        'category_labels':category_labels,
        'category_values':category_values,
        'total_habits':len(user_habits),
        'progress_data':progress_data[:5],
        'habit_gems': sum(habit.count for habit in user_habits),
        'habit_cards':user_habits,
        'motivational_message': random.choice(motivational_messages),
        'highest_streak':highest_streak,
    }

    return render(request, 'habits/dashboard.html', context)

@login_required
def create_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            print(request.user)
            habit.save()
            # manual trigger for initializing a habit analytics database
            post_save.send(sender=Habit, instance=habit, habit_initialized=True)
            return redirect('habits:dashboard')
        else:
            print(form.errors)
    else:
        form = HabitForm()
    return render(request, 'habits/create_habit.html', {'form': form})

@login_required
def delete_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    if request.method == 'POST':
        habit.is_active = False
        habit.save()
        return redirect('habits:dashboard')
    return render(request, 'habits/delete_habit.html', {'habit': habit})

@login_required
def mark_log(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    print(habit.name)
    if request.method == 'POST':
        habit.count += 1
        flag = request.POST.get('reset_and_log') == 'True'
        if flag:
            habit.set_remainder(True) # next task date reset.
        else:
            habit.set_remainder()
        habit.save()
        # manual trigger for analytics:signals
        post_save.send(sender=Habit, instance=habit, task_marked=True)
        return redirect('habits:dashboard')
    else:
        if habit.nxt_task_at.date() == now().date():
            message = f"Are you ready to mark today’s habit as complete? Tap 'Confirm' to log your progress!"
            context = {
                'message':message,
                'flag':False,
                'habit':habit,
            }
        else:
            message = f"Your next scheduled activity for this habit is on {habit.nxt_task_at.date()}. Would you like to reset it and log today's progress?"
            context = {
                'message':message,
                'flag':True,
                'habit':habit,
            }
    return render(request, 'habits/mark_log.html', context)