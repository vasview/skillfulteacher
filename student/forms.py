from cProfile import label
from winreg import KEY_READ
from django import forms
from tkinter import Widget
from urllib import request
from phonenumber_field.formfields import PhoneNumberField
from pkg_resources import require
from .models import *
from people.models import *
from django.forms.widgets import DateInput

class UpdatePersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['last_name', 'first_name', 'middle_name', 'birth_date', 'gender', 
                  'city', 'region', 'nationality', 'registration_address', 'actual_address',
                  'phone', 'photo']

        labels = {'last_name': 'Фамилия', 'first_name': 'Имя', 'middle_name':'Отчество', 'birth_date': 'Дата рождения',
                  'gender': 'Пол', 'city': 'Город', 'region': 'Область', 'nationality': 'Национальность',
                   'registration_address': 'Адрес прописки',  'actual_address': 'Адрес проживания',
                   'phone': 'Номер телефона', 'photo': 'Фотография'}
        
        widgets = {
            'last_name': forms.TextInput(attrs={"class":"w-50 form-control"}),
            'first_name': forms.TextInput(attrs={"class":"w-50 form-control"}),
            'middle_name': forms.TextInput(attrs={"class":"w-50 form-control"}),
            'birth_date': DateInput(attrs={'class': 'w-50 form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'gender': forms.Select(attrs={'class':'w-50 form-control form-select'}),
            'city': forms.Select(attrs={'class': 'w-50 form-control form-select'}),
            'region': forms.Select(attrs={'class': 'w-50 form-control form-select'}),
            'nationality': forms.Select(attrs={'class': 'w-50 form-control form-select'}),
            'registration_address': forms.TextInput(attrs={"class":"w-50 form-control"}),
            'actual_address': forms.TextInput(attrs={"class":"w-50 form-control"}),
            'phone': forms.TextInput(attrs={"class":"w-50 form-control"})
        }

class AddPersonForm(forms.Form):
    CHOICES = (
        ('NA', 'Не задано'),
        ('M', 'Мужчина'),
        ('F', 'Женщина')
    )
    last_name = forms.CharField(label='Фамилия', min_length=1, max_length=100, required=True, 
        widget=forms.TextInput(attrs={"class":"w-50 form-control"}))
    first_name = forms.CharField(label='Имя', min_length=2, max_length=100, required=True,
        widget=forms.TextInput(attrs={"class":"w-50 form-control"}))
    middle_name = forms.CharField(label='Отчество', max_length=100, required=False,
        widget=forms.TextInput(attrs={"class":"w-50 form-control"}))
    birth_date = forms.DateField(label='Дата рождения', required=False,
            widget=DateInput(attrs={'class': 'w-50 form-control'})
    )
    gender = forms.CharField( 
        label='Пол',
        required=False, 
        widget=forms.Select(choices=CHOICES, attrs={'class':'w-50 form-control form-select'})
    )
    city = forms.ModelChoiceField(label='Город', 
        queryset=City.objects.all(), 
        initial=None, 
        empty_label='Выберите город',
        required=False,
        widget=forms.Select(attrs={'class': 'w-50 form-control form-select'})
    )
    region = forms.ModelChoiceField(label='Область',
        queryset=Region.objects.all(), 
        initial=None, 
        empty_label='Выберите область',
        required=False,
        widget=forms.Select(attrs={'class': 'w-50 form-control form-select'})
    )
    nationality = forms.ModelChoiceField(label='Национальность',
        queryset=Nationality.objects.all(), 
        initial=None, 
        empty_label='Выберите национальность',
        required=False,
        widget=forms.Select(attrs={'class': 'w-50 form-control form-select'})
    )
    registration_address = forms.CharField(label='Адрес прописки', max_length=200, required=False,
        widget=forms.TextInput(attrs={"class":"w-50 form-control"}))
    actual_address = forms.CharField(label='Адрес проживания', max_length=200, required=False,
        widget=forms.TextInput(attrs={"class":"w-50 form-control"}))
    # phone = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': ('Phone')}), label=("Phone number"), required=False)
    phone = forms.CharField(label='Номер телефона', max_length=16, required=False,
        widget=forms.TextInput(attrs={"class":"w-50 form-control"}))
    photo = forms.ImageField(label='Фотография', required=False)
        # widget=forms.FileInput(attrs={'class':'custom-file-input'}))

    def save(self, *args, **kwargs):
        person = Person(
            last_name = self.cleaned_data['last_name'],
            first_name = self.cleaned_data['first_name'],
            middle_name = self.cleaned_data['middle_name'],
            birth_date = self.cleaned_data['birth_date'],
            gender = self.cleaned_data['gender'],
            city = self.cleaned_data['city'],
            region = self.cleaned_data['region'],
            nationality = self.cleaned_data['nationality'],
            registration_address = self.cleaned_data['registration_address'],
            actual_address = self.cleaned_data['actual_address'],
            phone = self.cleaned_data['phone'],
            photo = self.cleaned_data['photo']
        )
        person.save()
        return person

class AddStudentForm(AddPersonForm):
   def save(self, *args, **kwargs):
        person = super().save( *args, **kwargs)
        student = Student.objects.create(person=person)
        return student


class AddParentForm(AddPersonForm):
    relation_type = forms.CharField(label='Вид родства',
        required=False, 
        widget=forms.Select(choices=ParrentType.choices, attrs={'class':'w-50 form-control form-select'})
    )

    def save(self, *args, **kwargs):
        person = super().save( *args, **kwargs)
        person.contact_type = ContactType.PARENT
        person.save()
        relation = self.cleaned_data['relation_type']
        parent = Parent.objects.create(person=person, relation_type=relation)
        return parent

class StudentPortfolioForm(forms.ModelForm):
    class Meta:
        model = StudentReview
        fields = [ 'title','characteristic',]
        labels = {'title': 'Название', 'characteristic': 'характеристика'} 
