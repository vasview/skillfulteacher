from django.urls import path
from .views import *

urlpatterns = [
    path('', SchoolHome.as_view(), name='home'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('klass/<int:klass_id>/', show_klass, name='klass')
]