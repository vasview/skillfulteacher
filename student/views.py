from django.shortcuts import render
from django.http import HttpResponse


def students(request):
    return render(request, 'school/index.html')

def show_student(request, student_id):
    return render(request, 'school/index.html')
