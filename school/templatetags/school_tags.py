import imp
from django import template
from school.models import *
from staff.models import *

register = template.Library()

@register.simple_tag(name='get_subjects')
def get_subjects(filter=None):
    if not filter:
        return Subject.objects.all()
    else:
        return Subject.objects.filter(pk=filter)

@register.simple_tag(name='get_teachers')
def get_teachers(filter=None):
    if not filter:
        return Teacher.objects.all()
    else:
        return Teacher.objects.filter(pk=filter)