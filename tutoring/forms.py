from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Availability, User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ('day_of_week', 'start_time', 'end_time')
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
