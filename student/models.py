from contextlib import nullcontext
from distutils.command.upload import upload
from email.policy import default
from pickle import TRUE
from statistics import mode
from tabnanny import verbose
from tkinter import CASCADE
from turtle import back
from typing import ChainMap, OrderedDict
from django.db import models
from django.forms import CharField
from django.core.validators import MaxValueValidator, MinValueValidator 

class ParrentType(models.TextChoices):
    NONE = 'NA', 'Не выбрано'
    MOTHER = 'MOM', 'Мама'
    FATHER = 'DAD', 'Папа'
    CUSTODIAN = 'CSD', 'Опекун'

class Student(models.Model):
    person = models.OneToOneField('people.Person', on_delete=models.CASCADE, primary_key=True)
    klasses = models.ManyToManyField(
        'school.Klass',
        through = 'StudentKlass'
    )
    characteristics = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Список Учеников'
        ordering = ['person__full_name']

    def __str__(self):
        return "%s %s %s" % (self.person.last_name, self.person.first_name, self.person.middle_name)

class Parrent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    person = models.OneToOneField('people.Person', on_delete=models.CASCADE, primary_key=True)
    relation_type = models.CharField(
        max_length=3,
        choices=ParrentType.choices,
        default=ParrentType.NONE,
    )

    class Meta:
        verbose_name = 'Родитель'
        verbose_name_plural = 'Список Родителей'
        ordering = ['person__full_name']

    def __str__(self):
        return "%s %s %s" % (self.person.last_name, self.person.first_name, self.person.middle_name)

class StudentKlass(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    klass = models.ForeignKey('school.Klass', on_delete=models.CASCADE)
    date_from = models.DateField(auto_now_add=True)
    date_to = models.DateField()

    class Meta:
        verbose_name = 'Класс учеников'
        verbose_name_plural = 'Список классов учеников'
        ordering = ['klass__code', 'student__person__full_name']

    def __str__(self):
        return self.klass.code + ' ' + self.student.person.full_name

class StudentDocument(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="student_docs/%Y/%m%d/")
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Документ ученика'
        verbose_name_plural = 'Список документов ученика'
        ordering = ['name']

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=255)
    klass = models.ForeignKey('school.Klass', on_delete=models.CASCADE)
    teacher = models.ForeignKey('staff.Teacher', on_delete=models.SET_NULL, blank=True, null=True)
    subject = models.ForeignKey('school.Subject', on_delete=models.SET_NULL, blank=True, null=True)
    lessons = models.ManyToManyField('school.Lesson', through='GroupLesson')

    class Meta:
        verbose_name = 'Группа учеников'
        verbose_name_plural = 'Список групп учеников'
        ordering = ['name']

    def __str__(self):
        return self.name

class StudentGroup(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class GroupLesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    lesson = models.ForeignKey('school.Lesson', on_delete=models.CASCADE)

class GradeBook(models.Model):
    date = models.DateField(auto_now_add=True)
    subject = models.ForeignKey('school.Subject', on_delete=models.CASCADE)
    schoolyear = models.ForeignKey('school.SchoolYear', on_delete=models.SET_NULL, blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
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
        verbose_name = 'Табель посещения учеников'
        verbose_name_plural = 'Табеля посещамости учеников'
        ordering = ['student__person__last_name', 'lesson__subject__name', 'date']

    def __str__(self):
        return self.student.person.full_name + ' ' + self.lesson.name
        