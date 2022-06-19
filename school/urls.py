from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', SchoolHome.as_view(), name='home'),
    re_path(r'^login/$', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('klasses/', AllKlasses.as_view(), name='all_klasses'),
    path('klasses/<int:id>/', ShowKlass.as_view(), name='show_klass'),
    path('klasses/<int:id>/export_to_excel', export_students_xls, name='export_students_excel'),
    path('klasses/<int:id>/students/add', AddStudentsInKlass.as_view(), name='add_students_klass'),
    path('klasses/<int:id>/students/<int:std_id>/remove', RemoveStudentFromKlass.as_view(), name='remove_student_klass'),

    path('klasses/<int:id>/groups/add', AddKlassGroup.as_view(), name='add_klass_group'),
    path('klasses/<int:id>/groups/<int:group_id>/remove', RemoveKlassGroup.as_view(), name='remove_klass_group'),
    path('klasses/<int:id>/groups/<int:group_id>/edit', EditKlassGroup.as_view(), name='edit_klass_group'),

    path('groups/<int:id>/students/add', AddStudentsToGroup.as_view(), name='add_students_to_group'),
]