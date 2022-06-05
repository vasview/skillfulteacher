from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('teachers/', StaffTeachers.as_view(), name='teachers'),
    path('teachers/<int:id>', ShowTeacher.as_view(), name='show_teacher'),
    path('teachers/<int:id>/edit', EditTeacher.as_view(), name='edit_teacher'),
    path('teachers/<int:id>/documents/', ListTeacherDocuments.as_view(), name='list_teacher_document'),
    path('teachers/<int:id>/add_document', AddTeacherDocument.as_view(), name='add_teacher_document'),
    path('teachers/<int:id>/docs/<int:doc_id>/delete', DeleteTeacherDocument.as_view(), name='delete_teacher_document'),
    path('teachers/<int:id>/docs/<int:doc_id>/edit', EditTeacherDocument.as_view(), name='edit_teacher_document'),
]