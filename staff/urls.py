from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('teachers/', StaffTeachers.as_view(), name='teachers'),
    path('teachers/<int:teacher_id>', ShowTeacher.as_view(), name='show_teacher'),
]