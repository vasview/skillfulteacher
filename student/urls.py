from django.urls import path
from .views import *

urlpatterns = [
    path('', students),
    path('<int:student_id>', show_student),
]