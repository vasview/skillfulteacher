from contextlib import nullcontext
from distutils.command.upload import upload
from email.policy import default
from hashlib import blake2b
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
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from people.models import Gender

class JobPosition(models.Model):
    title = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Справочник должностей'
        ordering = ['title']

    def __str__(self):
        return self.title

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=350, blank=True, editable=False)
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
        verbose_name = 'Учитель'
        verbose_name_plural = 'Педагогический состав'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return "%s %s %s" % (self.first_name, self.middle_name, self.last_name)

class TeacherDocument(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="attachments/%Y/%m%d/")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Документ педагога'
        verbose_name_plural = 'Список документов педагоков'

    def __str__(self):
        return self.name

class JobPositionChange(models.Model):
    job_position = models.ForeignKey(JobPosition, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date_from = models.DateField(auto_now_add=True)
    date_to = models.DateField()

