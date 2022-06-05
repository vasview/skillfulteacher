from django.urls import path, include
from .views import *

urlpatterns = [
    path('', list_reports, name='reports'),
]