from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', SchoolHome.as_view(), name='home'),
    re_path(r'^login/$', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('klasses/', AllKlasses.as_view(), name='all_klasses'),
    path('klasses/<int:id>/', ShowKlass.as_view(), name='show_klass'),
    path('klasses/<int:id>/students/add', AddStudentsInKlass.as_view(), name='add_students_klass'),
    path('klasses/<int:id>/students/<int:std_id>/remove', RemoveStudentFromKlass.as_view(), name='remove_student_klass'),
]