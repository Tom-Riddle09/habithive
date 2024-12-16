from django.shortcuts import render, get_object_or_404
from habits.models import Habit
from .models import HabitAnalytics,OverallAnalytics
from datetime import datetime, timedelta
import json

def overall_analytics(request):
    analytics = get_object_or_404(OverallAnalytics,user=request.user) 
    # gather last 30 days activity log
    last_thirty = datetime.now().date() - timedelta(days=30)
    date_list, count_list = [],[]
    for key,count in analytics.activity_log.items():
        log_date = datetime.strptime(key, "%Y-%m-%d").date()
        print(log_date)

        # check if log_date is within last 30 days
        if last_thirty <= log_date <= datetime.now().date():
            date_list.append(log_date)
            count_list.append(count)
    # sorting both the list 
    sorted_data = sorted(zip(date_list,count_list), key=lambda x:x[0])
    date_list,count_list = zip(*sorted_data) if sorted_data else ([],[])

    # converting date list to str data type
    date_list = [date.strftime('%Y-%m-%d') for date in date_list]

    context = {
        'overall_data':analytics,
        'date_list': list(date_list),
        'count_list': list(count_list),
    }
    return render(request, 'analytics/overall_analytics.html', context)


def habit_analytics(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id)
    analytics_data = HabitAnalytics.objects.get(habit=habit)

    completed_days = analytics_data.completed_days
    missed_days = analytics_data.missed_days

    habit_dates = []
    for day in completed_days:
        habit_dates.append({
            'date': day,
            'status': 'completed'
        })
    for day in missed_days:
        habit_dates.append({
            'date': day,
            'status': 'missed'
        })   
    context = {
        'habit': habit,
        'analytics_data': analytics_data,
        'habit_dates': habit_dates,
        'habit_dates_chart': json.dumps(habit_dates),
        'recent_habits': habit_dates[:30],
    }
    return render(request, 'analytics/habit_analytics.html', context)