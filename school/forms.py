import imp
from django import forms
from .models import *

class LoginForm(forms.Form):
    user = forms.CharField(max_length=255, label='Пользователь')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')