from django.urls import path
from .views import *

urlpatterns = [
    path('', students, name='students'),
    path('new/', AddStudent.as_view(), name='add_student'),
    path('<int:student_id>', show_student, name='show_student'),
]