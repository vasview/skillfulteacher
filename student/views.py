import tempfile
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, CreateView, View, UpdateView
from student.forms import *
from student.models import *
from people.models import *
from django.forms.models import inlineformset_factory
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class ListStudents(LoginRequiredMixin, ListView):
    model = Person
    context_object_name = 'students'
    template_name = 'student/index.html'
    login_url = '/login/'

    def get_queryset(self):
        queryset = Person.objects.filter(contact_type='STD')
        return queryset

class ShowStudent(DetailView):
    model = Student
    context_object_name = 'student'
    pk_url_kwarg = 'id'
    template_name = 'student/show_student.html'

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
        )
        print(students)
    return render(request, 'student/index.html', { 'students': students})


# def show_student(request, id):
#     if request.GET:
#         student = Student.objects.get(pk=id)
#         form = AddPersonForm(Person.objects.filter(pk=student.person_id))

    # if request.method == 'POST':
    #     form = AddStudentForm(request.POST)
    #     if form.is_valid():
    #         print(form.cleaned_data)
    #         try:
    #             form.save()
    #             # Student.objects.get(pk=student_id)
    #             # return redirect('home')
    #         except:
    #             form.add_error(None, 'Ошибка добавления студента')
    # else:
    #     form = AddStudentForm()
    
    # return render(request, 'student/show_student.html', {'form': form})

StudentFormset = inlineformset_factory(
    Person, Student, fields=('active','characteristics')
)

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
        return get_object_or_404(Person, id=student.id)

    def get_success_url(self):
        id = self.kwargs.get('id')
        return reverse_lazy('show_student', kwargs={'id': id})

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     student = Student.objects.get(id=kwargs['id'])
    #     return student

    # def get(self,  request, *args, **kwargs):
    #     student = get_context_data(self, **kwargs)
    #     person = Student.objects.get(pk=student.id).person

    # def get(self, request, *args, **kwargs):
    #     # student = Student.objects.get(pk=request.GET['id'])
    #     student = Student.objects.get(pk=2)
    #     form = self.form_class(instance=student)
    #     return render(request, self.template_name, {'form': form})

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST,  request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("home")
    #     else:
    #         return render(request, self.template_name, {'form': form})
