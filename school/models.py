from email.policy import default
from pickle import TRUE
from statistics import mode
from tkinter import CASCADE
from typing import ChainMap
from django.db import models
from django.forms import CharField

class Gender(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Nationality(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Person(models.Model):
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    birthdate = models.DateField()
    registration_address = models.CharField(max_length=200)
    actual_address = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        return "%s %s %s" % (self.first_name, self.middle_name, self.last_name)

    def __str__(self):
        return self.get_full_name

class JobPosition(models.Model):
    title = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Teacher(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    job_positions = models.ManyToManyField(
        JobPosition,
        through = 'JobPositionChange'
    )
    active = models.BooleanField(default=True)

    def __str__(self):
         return "%s %s %s" % (self.person.first_name, self.person.middle_name, self.person.last_name)

class JobPositionChange(models.Model):
    job_position = models.ForeignKey(JobPosition, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date_from = models.DateField(auto_now_add=True)
    date_to = models.DateField()

class Subject(models.Model):
    name = models.CharField(max_length=100)
    teachers = models.ManyToManyField(
        Teacher,
        through = 'TeacherSubjects',
        through_fields = ('subject', 'teacher')
    )

    def __str__(self):
        return self.name

class TeacherSubjects(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    main = models.BooleanField(default=False)

class SchoolYear(models.Model):
    name = models.CharField(max_length=250)
    autumn_semester = models.DateField()
    spring_semester = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class SchoolLevel(models.Model):
    name = CharField(max_length=100)

    def __str__(self):
        return self.name

class Klass(models.Model):
    number = models.PositiveSmallIntegerField()
    letter = models.CharField(max_length=10)
    school_level = models.ForeignKey(SchoolLevel, on_delete=models.SET_NULL, blank=True, null=True)
    school_year = models.ForeignKey(SchoolYear, on_delete=models.SET_NULL, blank=True, null=True)
    classroom_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)
    active = models.BooleanField(default=True)

    @property
    def klass_number(self):
        return "%i %s" % (self.number, self.letter)

    def __str__(self):
        return self.get_klass_number

class KlassHistory(models.Model):
    klass = models.ForeignKey(Klass, on_delete=models.RESTRICT)
    number = models.PositiveSmallIntegerField()
    letter = models.CharField(max_length=10)
    school_level = models.ForeignKey(SchoolLevel, on_delete=models.SET_NULL, blank=True, null=True)
    school_year = models.ForeignKey(SchoolYear, on_delete=models.SET_NULL, blank=True, null=True)
    classroom_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ClassRoom(models.Model):
    number = models.CharField(max_length=50)
    level = models.SmallIntegerField()
 
    def __str__(self):
        return self.number

class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)