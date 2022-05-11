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

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(JobPosition)
admin.site.register(TeacherDocument)
