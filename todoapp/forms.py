from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, TextInput, DateInput, NumberInput, TimeInput, Select
from .models import Task



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    # last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2', )


class Task(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'deadline', 'not_until', 'order_within_project', 'duration_minutes', 'status']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'deadline': DateInput(attrs={'class': 'form-control datepicker'}),
            'not_until': DateInput(attrs={'class': 'form-control datepicker'}),
            'order_within_project': NumberInput(attrs={'class': 'form-control'}),
            'duration_minutes': TimeInput(attrs={'class': 'form-control'}),
            'status':  Select(attrs={'class': 'form-control'})
        }
        help_texts = {

        }

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
        self.fields['order_within_project'].required = True
        self.fields['name'].required = True
        self.fields['duration_minutes'].required = True