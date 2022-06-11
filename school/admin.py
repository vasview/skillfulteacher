from ast import Sub
from django.contrib import admin
from school.models import *

class ClassRoomTeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'klass', 'date_from', 'date_to')
    list_display_links = ('id', 'klass', 'teacher')

    def teacher(self, obj):
        return obj.teacher.full_name

    def klass(self, obj):
        return obj.klass.code


admin.site.register(SchoolLevel)
admin.site.register(SchoolYear)
admin.site.register(TeacherSubject)
admin.site.register(Subject)
admin.site.register(Klass)
admin.site.register(ClassRoom)
admin.site.register(ClassroomTeacher, ClassRoomTeacherAdmin)
admin.site.register(Lesson)
