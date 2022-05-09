from django.shortcuts import render

def teachers(request):
    return render(request, 'school/index.html')

def show_teacher(request, teacher_id):
    return render(request, 'school/index.html')
