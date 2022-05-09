from django.shortcuts import render
from django.http import HttpResponse


def persons(request):
    return render(request, 'school/index.html')

def show_person(request, student_id):
    return render(request, 'school/index.html')
