from ast import Sub
from asyncio.windows_events import NULL
from django.contrib import admin
from .models import *

class StudentAdmin(admin.ModelAdmin):
    list_display = ('person_id', 'last_name', 'first_name', 'middle_name', 'birth_date', 'active', 'klass', 'group')
    list_display_links = ('person_id', 'last_name')
    search_fields = ('person__last_name', 'person__first_name')
    list_editable = ('active',)
    # prepopulated_fields = {"full_name": ('last_name', 'first_name')}

    def last_name(self, obj):
        return obj.person.last_name
    
    def first_name(self, obj):
        return obj.person.first_name

    def middle_name(self, obj):
        return obj.person.middle_name

    def birth_date(self, obj):
        return obj.person.birth_date

    def klass(self, obj):
        if obj.klasses.all():
            return obj.klasses.all()[0].code
        else:
            return NULL
    
    def group(self, obj):
        if obj.groups.all():
            return obj.groups.all()[0].name
        else:
            return NULL
    
class StudentKlassAdmin(admin.ModelAdmin):
    list_display = ('klass_number', 'student_last_name')

    def klass_number(self, obj):
        return obj.klass.code

    def student_last_name(self, obj):
        return obj.student.person.last_name

admin.site.register(Student, StudentAdmin)
admin.site.register(Parent)
admin.site.register(StudentKlass, StudentKlassAdmin)
admin.site.register(StudentDocument)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(GradeBook)
admin.site.register(LessonAttendance)
