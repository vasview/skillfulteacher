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
from phonenumber_field.modelfields import PhoneNumberField

class Gender(models.TextChoices):
    NONE = 'NA', 'Не задано'
    MALE = 'M', 'Мужчина'
    FEMALE = 'F', 'Женщина'

class ContactType(models.TextChoices):
    NONE = 'NON', 'Не задано'
    STUDENT = 'STD', 'Студент'
    PARENT = 'PRT', 'Родитель'

class City(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Города'
        verbose_name_plural = 'Справочник городов'
        ordering = ['name']

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Области'
        verbose_name_plural = 'Справочник областей'
        ordering = ['name']

    def __str__(self):
        return self.name

class Nationality(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Национальности'
        verbose_name_plural = 'Справочник национальностей'
        ordering = ['name']

    def __str__(self):
        return self.name

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=350, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=2,
        choices=Gender.choices,
        default=Gender.NONE,
    )
    personal_number = models.SmallIntegerField(blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, blank=True, null=True)
    registration_address = models.CharField(max_length=200, blank=True, null=True)
    actual_address = models.CharField(max_length=200, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True)
    contact_type = models.CharField(
        max_length=3,
        choices=ContactType.choices,
        default=ContactType.STUDENT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self):
        if not self.middle_name:
            self.full_name = self.last_name + ' ' + self.first_name
        else:
            self.full_name = self.last_name + ' ' + self.first_name + ' ' + self.middle_name
        super(Person, self).save()

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Список контактов'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.full_name
