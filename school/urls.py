from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', SchoolHome.as_view(), name='home'),
    re_path(r'^login/$', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('klass/<int:klass_id>/', show_klass, name='klass'),
]