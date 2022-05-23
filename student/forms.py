from cProfile import label
from django import forms
from tkinter import Widget
from urllib import request
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from pkg_resources import require
from .models import *
from people.models import *

class UpdatePersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'birth_date']
        # widgets = {
        #     'characteristics': forms.Textarea(attrs={'cols':60, 'rows':10})
        # }
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'birth_date': 'Дата рождения'}

class AddStudentForm(forms.Form):
    CHOICES = (
        ('NA', 'Не задано'),
        ('M', 'Мужчина'),
        ('F', 'Женцина')
    )
    last_name = forms.CharField(label='Фамилия', min_length=1, max_length=100, required=True, 
        widget=forms.TextInput(attrs={"class":"w-50 form-control"}))
    first_name = forms.CharField(label='Имя', min_length=2, max_length=100, required=True,
        widget=forms.TextInput(attrs={"class":"w-50 form-control"}))
    middle_name = forms.CharField(label='Отчество', max_length=100, required=False,
        widget=forms.TextInput(attrs={"class":"w-50 form-control"}))
    birth_date = forms.DateField(label='Дата рождения', required=False,
            widget=forms.DateTimeInput(attrs={
            'class': 'w-50 form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    gender = forms.CharField( 
        label='Пол',
        required=False, 
        widget=forms.Select(choices=CHOICES, attrs={'class':'w-50 form-control'})
    )
    city = forms.ModelChoiceField(label='Город', 
        queryset=City.objects.all(), 
        initial=None, 
        empty_label='Выберите город',
        required=False,
        widget=forms.Select(attrs={'class': 'w-50 form-control'})
    )
    region = forms.ModelChoiceField(label='Область',
        queryset=Region.objects.all(), 
        initial=None, 
        empty_label='Выберите область',
        required=False,
        widget=forms.Select(attrs={'class': 'w-50 form-control'})
    )
    nationality = forms.ModelChoiceField(label='Национальность',
        queryset=Nationality.objects.all(), 
        initial=None, 
        empty_label='Выберите национальность',
        required=False,
        widget=forms.Select(attrs={'class': 'w-50 form-control'})
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
        student = Student.objects.create(person=person)
        return student
   