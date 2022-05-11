from django.contrib import admin

from .models import *

class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'middle_name', 'photo')
    list_display_links = ('id', 'last_name')
    search_fields = ('last_name', 'first_name')
    # list_editable = ('city',)
    # prepopulated_fields = {"full_name": ('last_name', 'first_name')}


admin.site.register(City)
admin.site.register(Region)
admin.site.register(Nationality)
admin.site.register(Person, PersonAdmin)