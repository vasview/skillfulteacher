import imp
from django import forms

from student.models import Group
from .models import *
from django.forms.widgets import DateInput
from tinymce.widgets import TinyMCE

class UpdateTeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['last_name', 'first_name', 'middle_name', 'birth_date', 'gender', 'phone', 'avatar']

        labels = {'last_name': 'Фамилия', 'first_name': 'Имя', 'middle_name':'Отчество', 'birth_date': 'Дата рождения',
                  'gender': 'Пол', 'phone': 'Номер телефона', 'avatar': 'Аватар'}
        
        widgets = {
            'last_name': forms.TextInput(attrs={"class":"w-50 form-control"}),
            'first_name': forms.TextInput(attrs={"class":"w-50 form-control"}),
            'middle_name': forms.TextInput(attrs={"class":"w-50 form-control"}),
            'birth_date': DateInput(attrs={'class': 'w-50 form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'gender': forms.Select(attrs={'class':'w-50 form-control'}),
            'phone': forms.TextInput(attrs={"class":"w-50 form-control"})
        }

class TeacherDocumentForm(forms.ModelForm):
    class Meta:
        model = TeacherDocument
        fields = [ 'name','file',]
        labels = {'name': 'Название', 'file': 'Документ'} 

        widgets = {
            'name': forms.TextInput(attrs={"class":"w-50 form-control"}),
        }

class LessonPlanForm(forms.ModelForm):
    class Meta:
        model = LessonPlan
        fields = [ 'title','purpose', 'lesson_type', 'lesson_plan', 'lesson_flow']
        labels = {
            'title':        'Название', 
            'purpose':      'Цели', 
            'lesson_type':  'Тип урока', 
            'lesson_plan':  'План урока', 
            'lesson_flow':  'Ход урока',
        } 