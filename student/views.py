from email import utils
from email.policy import HTTP
from multiprocessing import get_start_method
import tempfile
from webbrowser import get
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, CreateView, View, UpdateView
import elklassproject
from student.forms import *
from student.models import *
from people.models import *
from django.forms.models import inlineformset_factory
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .mixins import *
from django.template.loader import get_template
from elklassproject.utils.html_to_pdf import render_to_pdf
import datetime
from django.template import loader
# from django_weasyprint import WeasyTemplateResponseMixin
# from django_weasyprint.views import WeasyTemplateResponse

class ListStudents(LoginRequiredMixin, ListView):
    model = Person
    context_object_name = 'students'
    template_name = 'student/index.html'
    login_url = '/login/'
    paginate_by = 10

    def get_queryset(self):
        queryset = Person.objects.filter(contact_type='STD')
        return queryset

class ShowStudent(LoginRequiredMixin, DetailView):
    model = Student
    context_object_name = 'student'
    pk_url_kwarg = 'id'
    template_name = 'student/show_student.html'
    login_url = '/login/'

@login_required()
def search_students(request):
    # search_vector = SearchVector('first_name', 'last_name')
    # if ('query' in request.GET) and request.GET['query'].strip():
    #     query_string=request.GET['query']
    #     students = Person.objects.annotate(
    #             search=search_vector).filter(search=query_string)
   
    if ('query' in request.GET) and request.GET['query'].strip():
        query_string=request.GET['query']
        students = Person.objects.filter(
                Q(first_name__icontains=query_string) | Q(last_name__icontains=query_string)
        ).filter(contact_type='STD')
    return render(request, 'student/index.html', { 'students': students})

class AddStudent(LoginRequiredMixin, View):
    form_class = AddStudentForm
    template_name = 'student/add_student.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST,  request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            return render(request, self.template_name, {'form': form})

class EditStudent(LoginRequiredMixin, UpdateView):
    form_class = UpdatePersonForm
    template_name = 'student/edit_student.html'
    pk_url_kwarg = 'id'
    login_url = '/login/'

    def get_object(self):
        id = self.kwargs.get('id')
        student = Student.objects.get(pk=id)
        return get_object_or_404(Person, id=student.person.id)

    def get_success_url(self):
        id = self.kwargs.get('id')
        return reverse_lazy('show_student', kwargs={'id': id})

# section related to Student Parents
class ShowParent(LoginRequiredMixin, DetailView):
    model = Parent
    context_object_name = 'parent'
    pk_url_kwarg = 'id'
    template_name = 'student/show_parent.html'
    login_url = '/login/'

class CreateParent(LoginRequiredMixin,View):
    form_class = AddParentForm
    template_name = 'student/add_parent.html'
    login_url = '/login/'

    def get_student(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Student, id=id)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        student = self.get_student()
        return render(request, self.template_name, {'form': form, 'student': student})

    def post(self, request, *args, **kwargs):
        student = self.get_student()
        form = self.form_class(request.POST,  request.FILES)
        if form.is_valid():
            parent = form.save()
            student.parents.add(parent)
            return redirect('show_student', id = student.id)
        else:
            return render(request, self.template_name, {'form': form, 'student': student})

class EditParent(LoginRequiredMixin, UpdateView):
    form_class = UpdatePersonForm
    template_name = 'student/edit_parent.html'
    pk_url_kwarg = 'id'
    login_url = '/login/'

    def get_object(self):
        id = self.kwargs.get('id')
        parent = Parent.objects.get(pk=id)
        return get_object_or_404(Person, id=parent.person.id)

    def get_success_url(self):
        id = self.kwargs.get('id')
        return reverse_lazy('show_parent', kwargs={'id': id})

class DeleteParent(LoginRequiredMixin, DeleteView):
    model = Parent
    pk_url_kwarg = 'parent_id'
    template_name = 'student/confirm_delete.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'родителя'
        return context

    def get_success_url(self):
        id = self.kwargs.get('id')
        return reverse_lazy('show_student', kwargs={'id': id})


### section related to student characteristics ###
class CreateStudentReview(LoginRequiredMixin, View):
    form_class = StudentPortfolioForm
    template_name = 'student/create_characteristic.html'
    login_url = '/login/'

    def get_student(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Student, id=id)

    def get(self, request, *args, **kwargs):
        student = self.get_student()
        teacher = request.user
        form = self.form_class()
        context = {
            'form': form, 
            'student': student,
            'teacher': teacher
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        student = self.get_student()
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.student = student
            form.instance.teacher = request.user.teacher
            form.save()
            return redirect('show_student', id = student.id)
        else:
            return render(request, self.template_name, {'form': form, 'student': student})

class ShowStudentReview(LoginRequiredMixin, DetailView):
    model = StudentReview
    context_object_name = 'review'
    pk_url_kwarg = 'id'
    template_name = 'student/show_characteristic.html'
    login_url = '/login/'

class EditStudentReview(LoginRequiredMixin, UpdateView):
    form_class = StudentPortfolioForm
    context_object_name = 'review'
    template_name = 'student/edit_characteristic.html'
    pk_url_kwarg = 'id'
    login_url = '/login/'

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(StudentReview, pk=id)

    def get_success_url(self):
        id = self.kwargs.get('id')
        return reverse_lazy('show_review', kwargs={'id': id})

class DeleteStudentReview(LoginRequiredMixin, DeleteView):
    model = StudentReview
    pk_url_kwarg = 'review_id'
    template_name = 'student/confirm_delete.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'характеристику ученика'
        return context

    def get_success_url(self):
        id = self.kwargs.get('id')
        return reverse_lazy('show_student', kwargs={'id': id})

### section related to student documents ###
class AddStudentDocument(LoginRequiredMixin, View):
    form_class = StudentDocumentForm
    template_name = 'student/add_student_document.html'
    login_url = '/login/'

    def get_student(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Student, id=id)

    def get(self, request, *args, **kwargs):
        student = self.get_student()
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'student': student})

    def post(self, request, *args, **kwargs):
        student = self.get_student()
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.instance.student = student
            form.save()
            return redirect('show_student', id = student.id)
        else:
            return render(request, self.template_name, {'form': form, 'student': student})

class EditStudentDocument(LoginRequiredMixin, UpdateView):
    form_class = StudentDocumentForm
    context_object_name = 'document'
    template_name = 'student/edit_student_document.html'
    pk_url_kwarg = 'doc_id'
    login_url = '/login/'

    def get_object(self):
        id = self.kwargs.get('doc_id')
        return get_object_or_404(StudentDocument, pk=id)

    def get_success_url(self):
        id = self.kwargs.get('id')
        return reverse_lazy('show_student', kwargs={'id': id})

class DeleteStudentDocument(LoginRequiredMixin, DeleteView):
    model = StudentDocument
    pk_url_kwarg = 'doc_id'
    template_name = 'student/confirm_delete.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'документ ученика'
        return context

    def get_success_url(self):
        id = self.kwargs.get('id')
        return reverse_lazy('show_student', kwargs={'id': id})

# related to print Characteristic of a Student

class GenerateStudentCharacteristicPDF(View):
    template_name = 'student/pdf/print_student_characteristic.html'

    def get_student_review(self):
        id = self.kwargs.get('id')
        return get_object_or_404(StudentReview, id=id)

    def get(self, request, *args, **kwargs):

        template = self.template_name
        context = {
            'review': self.get_student_review(),
            'teacher': request.user.teacher,
            'today': datetime.date.today()
        }
        # filename = 'student_review.pdf'

        pdf = render_to_pdf(template, context)
        return HttpResponse(pdf, content_type='application/pdf')

