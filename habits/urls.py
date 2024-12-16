from django.urls import path
from . import views

app_name = 'habits'


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_habit, name='create_habit'),
    path('delete/<int:habit_id>/', views.delete_habit, name='delete_habit'),
    path('mark-log/<int:habit_id>/', views.mark_log, name='mark_log'),
]