from ast import Sub
from django.contrib import admin
from school.models import City, Region, Nationality, Subject, JobPosition

admin.site.register(City)
admin.site.register(Region)
admin.site.register(Nationality)
admin.site.register(Subject)
admin.site.register(JobPosition)