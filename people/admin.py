from django.contrib import admin

from .models import *

admin.site.register(City)
admin.site.register(Region)
admin.site.register(Nationality)
admin.site.register(Person)