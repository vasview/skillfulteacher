from django import forms
from .models import *

class LoginForm(forms.Form):
    user = forms.CharField(max_length=50, label='Пользователь', 
                        widget=forms.TextInput(attrs={'class':'form-control', 'id':"floatingInput", 'placeholder':'Пользователь'}))
    password = forms.CharField(max_length=50, label='Пароль',
                        widget=forms.PasswordInput(attrs={'class':'form-control', 'id':"floatingPassword", 'placeholder':'Пароль'}))