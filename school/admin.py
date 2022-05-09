from ast import Sub
from django.contrib import admin
from school.models import *

admin.site.register(SchoolLevel)
admin.site.register(SchoolYear)
admin.site.register(TeacherSubject)
admin.site.register(Subject)
admin.site.register(Klass)
admin.site.register(ClassRoom)
admin.site.register(ClassroomTeacher)
admin.site.register(Lesson)
