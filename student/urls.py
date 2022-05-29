from django.urls import path
from .views import *

urlpatterns = [
    path('', ListStudents.as_view(), name='students'),
    path('new/', AddStudent.as_view(), name='add_student'),
    path('<int:id>', ShowStudent.as_view(), name='show_student'),
    path('<int:id>/edit', EditStudent.as_view(), name='edit_student'),
    path('<int:id>/add_parent', CreateParent.as_view(), name='add_student_parent'),
    path('search/', search_students, name='search_students'),
]