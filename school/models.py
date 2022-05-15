from contextlib import nullcontext
from distutils.command.upload import upload
from email.policy import default
from pickle import TRUE
from statistics import mode
from tabnanny import verbose
from tkinter import CASCADE
from turtle import back
from typing import ChainMap
from django.db import models
from django.forms import CharField
from django.core.validators import MaxValueValidator, MinValueValidator

class SchoolLevel(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Уровень школьного образования'
        verbose_name_plural = 'Справочник уровней школьного образования'
        ordering = ['id']

    def __str__(self):
        return self.name

class SchoolYear(models.Model):
    period = models.CharField(max_length=16, editable=False)
    autumn_semester = models.PositiveSmallIntegerField(
        default=2020, 
        validators=[MinValueValidator(2020), MaxValueValidator(2050)]
    )
    spring_semester = models.PositiveSmallIntegerField(
        default=2021, 
        validators=[MinValueValidator(2020), MaxValueValidator(2050)]
    )
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Учебный год'
        verbose_name_plural = 'Учебные года'
        ordering = ['-period']

    def save(self):
        self.period = str(self.autumn_semester) + '-' + str(self.spring_semester)
        super(SchoolYear, self).save()

    def __str__(self):
        return self.period

class Klass(models.Model):
    code = models.CharField(max_length=5, blank=True, null=True)
    number = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    letter = models.CharField(max_length=2)
    school_level = models.ForeignKey(SchoolLevel, on_delete=models.SET_NULL, blank=True, null=True)
    school_year = models.ForeignKey(SchoolYear, on_delete=models.SET_NULL, blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Список классов'
        ordering = ['code']

    def save(self):
        if not self.pk:
            self.code = str(self.number) + self.letter
        super(Klass, self).save()

    def __str__(self):
        return self.code

class Subject(models.Model):
    name = models.CharField(max_length=100)
    teachers = models.ManyToManyField(
        'staff.Teacher',
        through = 'TeacherSubject',
        through_fields = ('subject', 'teacher')
    )

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Справочник предметов'
        ordering = ['name']

    def __str__(self):
        return self.name

class TeacherSubject(models.Model):
    teacher = models.ForeignKey('staff.Teacher', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    main = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Предмет учителя'
        verbose_name_plural = 'Предметы учителей'
        ordering = ['subject__name', 'teacher__last_name']

    def __str__(self):
        return self.subject.name + ' ' + self.teacher.full_name

class ClassroomTeacher(models.Model):
    teacher = models.ForeignKey('staff.Teacher', on_delete=models.SET_NULL, blank=True, null=True)
    klass = models.ForeignKey(Klass, on_delete=models.SET_NULL, blank=True, null=True)
    date_from = models.DateField(auto_now_add=True)
    date_to = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Классный руководитель'
        verbose_name_plural = 'Классные руководители'
        ordering = ['klass__code']

    def __str__(self):
        return self.teacher.full_name + ' ' + self.klass.code

class KlassHistory(models.Model):
    klass = models.ForeignKey(Klass, on_delete=models.RESTRICT)
    number = models.PositiveSmallIntegerField()
    letter = models.CharField(max_length=10)
    school_level = models.ForeignKey(SchoolLevel, on_delete=models.SET_NULL, blank=True, null=True)
    school_year = models.ForeignKey(SchoolYear, on_delete=models.SET_NULL, blank=True, null=True)
    classroom_teacher = models.ForeignKey('staff.Teacher', on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ClassRoom(models.Model):
    number = models.CharField(max_length=10)
    level = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Справочник кабинетов'
        ordering = ['number']
 
    def __str__(self):
        return self.number

class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey('staff.Teacher', on_delete=models.SET_NULL, blank=True, null=True)
    schoolyear = models.ForeignKey(SchoolYear, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    classroom = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, blank=True, null=True)
    is_finished = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['schoolyear__autumn_semester', 'date', 'subject__name' ]

    def __str__(self):
        return self.subject.name
