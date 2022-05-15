from django.forms import ModelChoiceField
from django.views.generic import View, ListView, DetailView, CreateView
from django.shortcuts import render, get_object_or_404
from .models import *
from school.models import Subject

class StaffTeachers(ListView):
    model = Teacher
    template_name = 'staff/index.html'


class ShowTeacher(DetailView):
    model = Teacher
    template_name = 'staff/teacher_profile.html'
    pk_url_kwarg = 'teacher_id'
    context_object_name = 'teacher'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['my_subjects'] = Subject.objects.all()
        return context
