from contextlib import nullcontext
from distutils.command.upload import upload
from email.policy import default
import imp
from pickle import TRUE
from statistics import mode
from tabnanny import verbose
from tkinter import CASCADE
from turtle import back
from typing import ChainMap, OrderedDict
from django.db import models
from django.forms import CharField
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.urls import reverse
from tinymce.models import HTMLField

class ParrentType(models.TextChoices):
    NONE = 'NA', 'Не выбрано'
    MOTHER = 'MOM', 'Мама'
    FATHER = 'DAD', 'Папа'
    CUSTODIAN = 'CSD', 'Опекун'

class Student(models.Model):
    person = models.OneToOneField('people.Person', on_delete=models.PROTECT)
    klasses = models.ManyToManyField(
        'school.Klass',
        through = 'StudentKlass'
    )
    groups = models.ManyToManyField(
        'student.Group',
        through = 'student.GroupMember'
    )
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Ученики'
        verbose_name_plural = 'Список Учеников'
        ordering = ['person__full_name']

    def __str__(self):
        return "%s %s %s" % (self.person.last_name, self.person.first_name, self.person.middle_name)

    def get_absolute_url(self):
        return reverse('show_student', kwargs={'id': self.pk})

class StudentReview(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='reviews')
    teacher = models.ForeignKey('staff.Teacher', on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=255)
    characteristic = HTMLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Parent(models.Model):
    person = models.OneToOneField('people.Person', on_delete=models.PROTECT)
    students = models.ManyToManyField(Student, related_name='parents')
    relation_type = models.CharField(
        max_length=3,
        choices=ParrentType.choices,
        default=ParrentType.NONE,
    )

    class Meta:
        verbose_name = 'Родители'
        verbose_name_plural = 'Список Родителей'
        ordering = ['person__full_name']

    def __str__(self):
        return "%s %s %s" % (self.person.last_name, self.person.first_name, self.person.middle_name)

class StudentKlass(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    klass = models.ForeignKey('school.Klass', on_delete=models.PROTECT, related_name='students')
    date_from = models.DateField(auto_now_add=True)
    date_to = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Состав классов учеников'
        verbose_name_plural = 'Составы классов учеников'
        ordering = ['klass__code', 'student__person__full_name']

    def __str__(self):
        return self.klass.code + ' ' + self.student.person.full_name

class StudentDocument(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="student_docs/%Y/%m%d/")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Документы ученика'
        verbose_name_plural = 'Список документов ученика'
        ordering = ['name']

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=255, default='Unallocated')
    klass = models.ForeignKey('school.Klass', on_delete=models.PROTECT, blank=True, null=True)
    teacher = models.ForeignKey('staff.Teacher', on_delete=models.SET_NULL, blank=True, null=True)
    subject = models.ForeignKey('school.Subject', on_delete=models.SET_NULL, blank=True, null=True)
    lessons = models.ManyToManyField('school.Lesson', through='GroupLesson')

    class Meta:
        verbose_name = 'Группы учеников'
        verbose_name_plural = 'Список групп учеников'
        ordering = ['name']

    def __str__(self):
        return self.name

class GroupMember(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student_groups")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_members")

    class Meta:
        verbose_name = 'Состав группы учеников'
        verbose_name_plural = 'Состав групп учеников'

    def __str__(self):
        return self.group.name

class GroupLesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    lesson = models.ForeignKey('school.Lesson', on_delete=models.CASCADE)

class GradeBook(models.Model):
    date = models.DateField(auto_now_add=True)
    subject = models.ForeignKey('school.Subject', on_delete=models.PROTECT)
    schoolyear = models.ForeignKey('school.SchoolYear', on_delete=models.SET_NULL, blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    grade = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    first_trimester = models.DecimalField(max_digits = 3, decimal_places = 2, blank=True, null=True)
    second_trimester = models.DecimalField(max_digits = 3, decimal_places = 2, blank=True, null=True)
    third_trimester = models.DecimalField(max_digits = 3, decimal_places = 2, blank=True, null=True)
    fourth_trimester = models.DecimalField(max_digits = 3, decimal_places = 2, blank=True, null=True)
    final_grade = models.DecimalField(max_digits = 3, decimal_places = 2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Дневник ученика'
        verbose_name_plural = 'Дневники учеников'
        ordering = ['student__person__last_name', 'subject__name']
    
    def __str__(self):
        return self.student.person.full_name + ' ' + self.subject.name
    
class LessonAttendance(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    lesson = models.ForeignKey('school.Lesson', on_delete=models.CASCADE)
    schoolyear = models.ForeignKey('school.SchoolYear', on_delete=models.SET_NULL, blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_attended = models.BooleanField(default=True)
    reason = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Табель посещамости учеников'
        verbose_name_plural = 'Табеля посещамости учеников'
        ordering = ['student__person__last_name', 'lesson__subject__name', 'date']

    def __str__(self):
        return self.student.person.full_name + ' ' + self.lesson.name
        