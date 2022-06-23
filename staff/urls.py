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

    path('teachers/lesson_plans', ListTeachersLessonPlans.as_view(), name='all_teacher_lesson_plans'),
    path('teachers/<int:id>/lesson_plans/add', AddTeacherLessonPlan.as_view(), name='add_teacher_lesson_plan'),
    path('lesson_plans/<int:plan_id>/show', ShowTeacherLessonPlan.as_view(), name='show_teacher_lesson_plan'),
    path('lesson_plans/<int:plan_id>/edit', EditTeacherLessonPlan.as_view(), name='edit_teacher_lesson_plan'),
    path('lesson_plans/<int:plan_id>/print', GenerateLessonPlanPDF.as_view(), name='print_lesson_plan'),
    path('teachers/<int:id>/lesson_plans/<int:plan_id>/delete', DeleteTeacherLessonPlan.as_view(), name='delete_teacher_lesson_plan'),
]