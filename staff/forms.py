import imp
from django import forms
from .models import *

class UpdateTeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['last_name', 'first_name', 'middle_name', 'birth_date', 'gender', 'phone', 'avatar']

        labels = {'last_name': 'Фамилия', 'first_name': 'Имя', 'middle_name':'Отчество', 'birth_date': 'Дата рождения',
                  'gender': 'Пол', 'phone': 'Номер телефона', 'avatar': 'Аватарка'}
        
        widgets = {
            'last_name': forms.TextInput(attrs={"class":"w-50 form-control"}),
            'first_name': forms.TextInput(attrs={"class":"w-50 form-control"}),
            'middle_name': forms.TextInput(attrs={"class":"w-50 form-control"}),
            'birth_date': forms.DateInput(attrs={'class': 'w-50 form-control datetimepicker-input',
            'data-target': '#datetimepicker1'}),
            'gender': forms.Select(attrs={'class':'w-50 form-control'}),
            'phone': forms.TextInput(attrs={"class":"w-50 form-control"})
        }