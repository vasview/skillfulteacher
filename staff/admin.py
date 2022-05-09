import re
from django.contrib import admin

from .models import *

admin.site.register(Teacher)
admin.site.register(JobPosition)
admin.site.register(TeacherDocument)
