from lib2to3.pgen2.pgen import DFAState
from multiprocessing.spawn import import_main_path
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView, CreateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from school.forms import *

class SchoolHome(View):
    def get(self,request,*args, **kwargs):
        return render(request, 'school/index.html')

def login_user(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            username = form.cleaned_data['user']
            password = form.cleaned_data['password']
            
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
            else:
                form.add_error(None, 'Ошибка входа')
    else:
        form = LoginForm()
    
    return render(request, 'school/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect(reverse_lazy('home'))

def show_klass(request, klass_id):
    klass = get_object_or_404(pk=klass_id)

    context = {
        'klass': klass
    }

    return render(request, 'school/klass.html', context=context)