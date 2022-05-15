from lib2to3.pgen2.pgen import DFAState
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, CreateView
from school.forms import *

class SchoolHome(View):
    def get(self,request,*args, **kwargs):
        return render(request, 'school/index.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            try:
                User.objects.get(login=form.user)
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка входа')
    else:
        form = LoginForm()
    
    return render(request, 'school/login.html', {'form': form})

def show_klass(request, klass_id):
    klass = get_object_or_404(pk=klass_id)

    context = {
        'klass': klass
    }

    return render(request, 'school/klass.html', context=context)