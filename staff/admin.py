from csv import list_dialects
import re
from django.contrib import admin

from .models import *

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'middle_name', 'user_active')
    list_display_links = ('id', 'last_name')
    search_fields = ('last_name', 'first_name')
    # list_editable = ('user_active',)
    prepopulated_fields = {"full_name": ('last_name', 'first_name')}

    def user_active(self, obj):
        return obj.user.is_active

class TeacherDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'teacher')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'teacher')

    def teacher(self, obj):
        return obj.teacher.full_name

class JobPositionChangeAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_position', 'teacher', 'date_from', 'date_to')
    list_display_links = ('id', 'job_position', 'teacher')
    # search_fields = ('job_position', 'teacher')

    def teacher(self, obj):
        return obj.teacher.full_name

    def job_position(self, obj):
        return obj.job_position.title

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(JobPosition)
admin.site.register(TeacherDocument, TeacherDocumentAdmin)
admin.site.register(JobPositionChange, JobPositionChangeAdmin)
