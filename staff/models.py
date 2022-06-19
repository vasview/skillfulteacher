from contextlib import nullcontext
from distutils.command.upload import upload
from email.policy import default
from hashlib import blake2b
from lib2to3.pgen2.pgen import DFAState
from pickle import TRUE
from statistics import mode
from tabnanny import verbose
from tkinter import CASCADE
from tokenize import blank_re
from turtle import back
from typing import ChainMap
from django.db import models
from django.forms import CharField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from people.models import Gender
from student.models import Student
from tinymce.models import HTMLField

class JobPosition(models.Model):
    title = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Должности'
        verbose_name_plural = 'Справочник должностей'
        ordering = ['title']

    def __str__(self):
        return self.title

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=350, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=2,
        choices=Gender.choices,
        default=Gender.NONE,
    )
    phone = PhoneNumberField(blank=True, null=True)
    avatar = models.ImageField(upload_to="avatar/%Y/%m/%d/", blank=True, null=True)
    job_positions = models.ManyToManyField(
        JobPosition,
        through = 'JobPositionChange'
    )
    klasses = models.ManyToManyField(
        'school.Klass',
        through = 'school.ClassroomTeacher'
    )

    # @receiver(post_save, sender=User)
    # def create_user_teacher(sender, instance, created, **kwargs):
    #     if created and not instance.is_superuser:
    #         Teacher.objects.create(user=instance)

    # @receiver(post_save, sender=User)
    # def save_user_teacher(sender, instance, **kwargs):
    #     if not instance.is_superuser:
    #         instance.teacher.save()

    def save(self):
        self.full_name = self.last_name + ' ' + self.first_name + ' ' + self.middle_name
        super(Teacher, self).save()

    class Meta:
        verbose_name = 'Учителя'
        verbose_name_plural = 'Педагогический состав'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return "%s %s %s" % (self.first_name, self.middle_name, self.last_name)

    def get_absolute_url(self):
        return reverse('show_teacher', kwargs={'id': self.pk})

class TeacherDocument(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="attachments/%Y/%m%d/")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Документы учителя'
        verbose_name_plural = 'Список документов учителей'

    def __str__(self):
        return self.name

class JobPositionChange(models.Model):
    job_position = models.ForeignKey(JobPosition, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date_from = models.DateField(null=False)
    date_to = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'История смены должностей сотрудниками'
        verbose_name_plural = 'История смены должностей сотрудниками'
        ordering = ['job_position', 'date_from']

    def _str_(self):
        return "%s %s" % (self.teacher.full_name, self.job_position.title)

class TeacherStudent(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

class LessonPlan(models.Model):
    title = models.CharField(max_length=255)
    purpose = HTMLField(blank=True, null=True)
    lesson_type = models.CharField(max_length=255)
    lesson_plan = HTMLField(blank=True, null=True)
    lesson_flow = HTMLField(blank=True, null=True)
    lesson = models.ForeignKey('school.lesson', on_delete=models.SET_NULL, blank=True, null=True, related_name='teacher_plans')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True, related_name='lesson_plans')

    class Meta:
        verbose_name = 'План урока'
        verbose_name_plural = 'Планы уроков'

    def __str__(self):
        return self.title