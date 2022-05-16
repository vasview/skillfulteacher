from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DeleteView, CreateView, View
from student.forms import *
from student.models import *
from people.models import *
from django.forms.models import inlineformset_factory


def students(request):
    if request.user.is_authenticated:
        return render(request, 'student/index.html')
    else:
        return redirect('login')

def show_student(request, student_id):
    if request.method == 'POST':
        form = AddStudentForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            try:
                form.save()
                # Student.objects.get(pk=student_id)
                # return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления студента')
    else:
        form = AddStudentForm()
    
    return render(request, 'student/show_student.html', {'form': form})

StudentFormset = inlineformset_factory(
    Person, Student, fields=('active','characteristics')
)

class AddStudent(View):
    # model = Person
    # fields = ['first_name','last_name', 'middle_name',]
    # labels = {
    #     'first_name' : 'Имя', 'last_name': 'Фамилия'
    # }
    form_class = AddStudentForm
    template_name = 'student/add_student.html'

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

    # def get_context_data(self, **kwargs):
    #     # we need to overwrite get_context_data
    #     # to make sure that our formset is rendered
    #     data = super().get_context_data(**kwargs)
    #     if self.request.POST:
    #         # data = AddStudentForm(self.request.POST)
    #         data["student"] = AddStudentForm(self.request.POST)
    #     else:
    #         # data = AddStudentForm()
    #         data["student"] = AddStudentForm()
    #     return data

    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     if form.is_valid():
    #         self.object = form.save()
    #     student = context["student"]
    #     self.object = form.save()
    #     if student.is_valid():
    #         student.instance = self.object
    #         student.save()
    #     return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse("home")

    # def get_initial(self):
    #     if Person.objects.filter(owner=self.request.user).exists():
    #         user = self.request.user
    #         initial = super(AddProductView, self).get_initial()
    #         initial['store'] = Store.objects.get(owner=user)
    #         return initial 

# def add_student(request):
#     if request.method == 'POST':
#         form = AddStudentForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             try:
#                 form.save()
#                 # Student.objects.get(pk=student_id)
#                 return redirect('home')
#             except:
#                 form.add_error(None, 'Ошибка добавления студента')
#     else:
#         form = AddStudentForm()
    
#     return render(request, 'student/add_student.html', {'form': form})
