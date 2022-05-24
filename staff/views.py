import imp
from django.forms import ModelChoiceField
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from phonenumbers import format_out_of_country_calling_number
from .models import *
from school.models import Subject
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin

class StaffTeachers(ListView):
    model = Teacher
    template_name = 'staff/index.html'


class ShowTeacher(LoginRequiredMixin, DetailView):
    model = Teacher
    template_name = 'staff/teacher_profile.html'
    pk_url_kwarg = 'id'
    context_object_name = 'teacher'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the subject
        context['my_subjects'] = Subject.objects.all()
        return context

class EditTeacher(LoginRequiredMixin, UpdateView):
    form_class = UpdateTeacherForm
    template_name = 'staff/edit_teacher.html'
    pk_url_kwarg = 'id'
    context_object_name = 'teacher'
    login_url = '/login/'

    def get_object(self):
        pk = self.kwargs.get('id')
        return get_object_or_404(Teacher, id=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_subjects'] = Subject.objects.all()
        return context

    def get_success_url(self):
        id = self.kwargs.get('id')
        return reverse_lazy('show_teacher', kwargs={'id': id})
