from django.urls import path
from .views import *

urlpatterns = [
    path('teachers/', teachers),
    path('teachers/<int:teacher_id>', show_teacher),
]