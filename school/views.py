from lib2to3.pgen2.pgen import DFAState
from multiprocessing.spawn import import_main_path
from django.template import RequestContext
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

def user_login(request):
    next_page = ''
    if request.GET:
        next_page = request.GET['next']

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user']
            password = form.cleaned_data['password']
            
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                if next_page == "":
                    return redirect('home')
                else:
                    return redirect(next_page)
            else:
                form.add_error(None, 'Ошибка входа')
    else:
        form = LoginForm()
    
    return render(request, 'school/login.html', {'form': form, 'next': next_page})

def user_logout(request):
    logout(request)
    return redirect(reverse_lazy('home'))

### End points related to klasses in the School

def all_klasses(request):
    klasses = Klass.objects.all()
    context = {'klasses': klasses}
    return render(request, 'school/all_klasses.html', context=context)

def show_klass(request, klass_id):
    klass = get_object_or_404(pk=klass_id)

    context = {
        'klass': klass
    }

    return render(request, 'school/klass.html', context=context)