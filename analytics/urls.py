# urls.py in analytics app
from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('overall/', views.overall_analytics, name='overall_analytics'),
    path('habit/<int:habit_id>/', views.habit_analytics, name='habit_analytics'),
]
