import imp
from re import template
from django.forms import ModelChoiceField
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
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

### section related to student documents ###
class ListTeacherDocuments(LoginRequiredMixin, View):
    form_class = TeacherDocument
    template_name = 'staff/teacher_documents.html'

    def get_teacher(self):
        id = self.kwargs.get('id')
        teacher = Teacher.objects.get(pk=id)
        return get_object_or_404(Teacher, id=id)

    def get(self, request, *args, **kwargs):
        teacher = self.get_teacher()
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'teacher': teacher})

class AddTeacherDocument(LoginRequiredMixin, View):
    form_class = TeacherDocumentForm
    template_name = 'staff/add_teacher_document.html'
    login_url = '/login/'

    def get_teacher(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Teacher, id=id)

    def get(self, request, *args, **kwargs):
        teacher = self.get_teacher()
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'teacher': teacher})

    def post(self, request, *args, **kwargs):
        teacher = self.get_teacher()
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.instance.teacher = teacher
            form.save()
            return redirect('list_teacher_document', id = teacher.id)
        else:
            return render(request, self.template_name, {'form': form, 'teacher': teacher})

class EditTeacherDocument(LoginRequiredMixin, UpdateView):
    form_class = TeacherDocumentForm
    context_object_name = 'document'
    template_name = 'staff/edit_teacher_document.html'
    pk_url_kwarg = 'doc_id'
    login_url = '/login/'

    def get_object(self):
        id = self.kwargs.get('doc_id')
        return get_object_or_404(TeacherDocument, pk=id)

    def get_success_url(self):
        id = self.kwargs.get('id')
        return reverse_lazy('list_teacher_document', kwargs={'id': id})

class DeleteTeacherDocument(LoginRequiredMixin, DeleteView):
    model = TeacherDocument
    pk_url_kwarg = 'doc_id'
    template_name = 'staff/delete_confirmation.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'документ учителя'
        return context

    def get_success_url(self):
        id = self.kwargs.get('id')
        return reverse_lazy('list_teacher_document', kwargs={'id': id})
