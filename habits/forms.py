from django import forms
from .models import Habit

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name','description','category','duration','frequency','custom_days_gap',]

        widgets = {
            'category':forms.Select(attrs={'class': 'form-control'}),
            'frequency':forms.Select(attrs={'class': 'form-control'}),
            'duration':forms.NumberInput(attrs={'placeholder':'How long to be done, if weekly then 2 week etc. [Only Number]'}),
            'custom_days_gap':forms.NumberInput(attrs={'placeholder':'Only for custom frequency'}),

        }