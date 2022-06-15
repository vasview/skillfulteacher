from django.urls import path
from .views import *

urlpatterns = [
    path('', ListStudents.as_view(), name='students'),
    path('new/', AddStudent.as_view(), name='add_student'),
    path('<int:id>', ShowStudent.as_view(), name='show_student'),
    path('<int:id>/edit', EditStudent.as_view(), name='edit_student'),
    
    path('<int:id>/add_parent', CreateParent.as_view(), name='add_student_parent'),
    path('<int:id>/parents/<int:parent_id>/delete', DeleteParent.as_view(), name='delete_student_parent'),
    path('parents/<int:id>', ShowParent.as_view(), name='show_parent'),
    path('parents/<int:id>/edit', EditParent.as_view(), name='edit_parent'),

    path('<int:id>/add_characteristics', CreateStudentReview.as_view(), name='add_characteristics'),
    path('<int:id>/reviews/<int:review_id>/delete', DeleteStudentReview.as_view(), name='delete_student_review'),
    path('reviews/<int:id>', ShowStudentReview.as_view(), name='show_review'),
    path('reviews/<int:id>/edit', EditStudentReview.as_view(), name='edit_review'),
    path('reviews/<int:id>/print', GenerateStudentCharacteristicPDF.as_view(), name='print_student_review'),

    path('<int:id>/add_document', AddStudentDocument.as_view(), name='add_student_document'),
    path('<int:id>/docs/<int:doc_id>/delete', DeleteStudentDocument.as_view(), name='delete_student_document'),
    path('<int:id>/docs/<int:doc_id>/edit', EditStudentDocument.as_view(), name='edit_student_document'),

    path('search/', search_students, name='search_students'),
]