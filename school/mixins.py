from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'