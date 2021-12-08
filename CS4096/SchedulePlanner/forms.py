from django import forms
from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, CourseLog

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','first_name','last_name')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email','first_name','last_name')


class CourseLogForm(ModelForm):
    class Meta:
        model = CourseLog
        fields = ('course', 'user', 'date')
