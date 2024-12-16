from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.models import User

UserModel = get_user_model() # dyanamically get the user model


class Habit(models.Model):
    CATEGORY_CHOICES = [
        ('fitness','Fitness'),
        ('learning','Learning'),
        ('health','Health'),
        ('productivity','Productivity'),
        ('personal_development','Personal Development'),
        ('financial','Financial'),
        ('environmental','Environmental'),
        ('creative','Creative'),
        ('social','Social'),
        ('spiritual','Spiritual'),
        ('professional','Professional'),
    ]

    FREQUENCY_CHOICES = [
        ('daily','Daily'),
        ('weekly','Weekly'),
        ('monthly','Monthly'),
        ('custom','Custom'),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES)
    duration = models.PositiveIntegerField(help_text="No. of repetitions.") # value for duration.
    frequency = models.CharField(max_length=20,choices=FREQUENCY_CHOICES,default='daily') 
    custom_days_gap = models.PositiveIntegerField(blank=True,null=True,help_text="In days. (Custom Frequency)")
    count = models.IntegerField(default=0) # no of times completed.
    streak = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    nxt_task_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} [{self.category}]'
    
    def set_remainder(self,flag=False): # set remainder date for the user on the day of activity | call every time the remainder date is reached.
        if self.frequency == 'daily':
            next_in = 1 # task to be completed next in ( how many days ) - calculated for remiander and streak checking.
        elif self.frequency == 'weekly':
            next_in = 7
        elif self.frequency == 'monthly':
            next_in = 30
        elif self.frequency == 'custom' and self.custom_days_gap:
            next_in = self.custom_days_gap
        else:
            next_in = 1 # default
        # updating remainder date

        if flag: # flag active when date is reset to now.
            self.nxt_task_at = now() + timedelta(days=next_in)
        else:
            self.nxt_task_at = self.nxt_task_at + timedelta(days=next_in)
        self.save()


    def calculate_progress(self, completed_tasks):
        progress =  (completed_tasks / self.duration) * 100 
        return round(min(progress,100), 2)




