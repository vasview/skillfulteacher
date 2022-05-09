from django.urls import path
from .views import *

urlpatterns = [
    path('', persons),
    path('<int:student_id>', show_person),
]