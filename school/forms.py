from django import forms

from student.models import StudentKlass, Student
from .models import *
from student.models import Group, GroupMember

class LoginForm(forms.Form):
    user = forms.CharField(max_length=50, label='Пользователь', 
                        widget=forms.TextInput(attrs={'class':'form-control', 'id':"user", 'placeholder':'Пользователь'}))
    password = forms.CharField(max_length=50, label='Пароль',
                        widget=forms.PasswordInput(attrs={'class':'form-control', 'id':"password", 'placeholder':'Пароль'}))

class StudentKlassForm(forms.Form):
    class Meta: 
        model = StudentKlass
        klass = forms.IntegerField()
        student = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(StudentKlassForm, self).__init__(*args, **kwargs)
        initial = kwargs.get('initial', {})
        # self.fields = {**initial}
        self.klass = initial.get('klass', None)
        self.student = initial.get('student', None)


    def save(self, *args, **kwargs):
        self.fields
        obj =  StudentKlass(klass = self.klass, student = self.student)
        obj.save()
        return obj

class AddKlassGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'klass',]

class StudentGroupMemberForm(forms.Form):
    class Meta: 
        model = GroupMember
        group = forms.IntegerField()
        student = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(StudentGroupMemberForm, self).__init__(*args, **kwargs)
        initial = kwargs.get('initial', {})
        # self.fields = {**initial}
        self.group = initial.get('group', None)
        self.student = initial.get('student', None)

    def save(self, *args, **kwargs):
        self.fields
        obj =  GroupMember(group = self.group, student = self.student)
        obj.save()
        return obj