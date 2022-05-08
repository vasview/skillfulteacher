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
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Gender(models.TextChoices):
    NONE = 'NA', 'Не выбрано'
    MALE = 'M', 'Мужчина'
    FEMALE = 'F', 'Женцина'

class ParrentType(models.TextChoices):
    NONE = 'NA', 'Не выбрано'
    MOTHER = 'MOM', 'Мама'
    FATHER = 'DAD', 'Папа'
    CUSTODIAN = 'CSD', 'Опекун'

class City(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Справочник городов'
        ordering = ['name']

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Область'
        verbose_name_plural = 'Справочник областей'
        ordering = ['name']

    def __str__(self):
        return self.name

class Nationality(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Национальность'
        verbose_name_plural = 'Справочник национальностей'
        ordering = ['name']

    def __str__(self):
        return self.name

class JobPosition(models.Model):
    title = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Справочник должностей'
        ordering = ['title']

    def __str__(self):
        return self.title

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

class Person(models.Model):
    gender = models.CharField(
        max_length=2,
        choices=Gender.choices,
        default=Gender.MALE,
    )
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    registration_address = models.CharField(max_length=200)
    actual_address = models.CharField(max_length=200)
    phone = PhoneNumberField(blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        return "%s %s %s" % (self.first_name, self.middle_name, self.last_name)

    def __str__(self):
        return self.get_full_name

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

    def save(self):
        if not self.id:
            self.code = str(self.number) + self.letter
        super(Klass, self).save()

    def __str__(self):
        return self.code

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    phone = PhoneNumberField(blank=True)
    avatar = models.ImageField(upload_to="avatar/%Y/%m/%d/")
    job_positions = models.ManyToManyField(
        JobPosition,
        through = 'JobPositionChange'
    )
    klasses = models.ManyToManyField(
        Klass,
        through = 'ClassroomTeacher'
    )

    @receiver(post_save, sender=User)
    def create_user_teacher(sender, instance, created, **kwargs):
        if created and not instance.is_superuser:
            Teacher.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_teacher(sender, instance, **kwargs):
        if not instance.is_superuser:
            instance.teacher.save()

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'
        ordering = ['person__last_name', 'person__first_name']

    def __str__(self):
        return "%s %s %s" % (self.person.first_name, self.person.middle_name, self.person.last_name)

class TeacherDocument(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="attachments/%Y/%m%d/")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class JobPositionChange(models.Model):
    job_position = models.ForeignKey(JobPosition, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date_from = models.DateField(auto_now_add=True)
    date_to = models.DateField()

class Subject(models.Model):
    name = models.CharField(max_length=100)
    teachers = models.ManyToManyField(
        Teacher,
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
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    main = models.BooleanField(default=False)

class ClassroomTeacher(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)
    klass = models.ForeignKey(Klass, on_delete=models.SET_NULL, blank=True, null=True)
    date_from = models.DateField()
    date_to = models.DateField(blank=True, null=True)

class KlassHistory(models.Model):
    klass = models.ForeignKey(Klass, on_delete=models.RESTRICT)
    number = models.PositiveSmallIntegerField()
    letter = models.CharField(max_length=10)
    school_level = models.ForeignKey(SchoolLevel, on_delete=models.SET_NULL, blank=True, null=True)
    school_year = models.ForeignKey(SchoolYear, on_delete=models.SET_NULL, blank=True, null=True)
    classroom_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ClassRoom(models.Model):
    number = models.CharField(max_length=10)
    level = models.SmallIntegerField()

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Справочник кабинетов'
        ordering = ['number']
 
    def __str__(self):
        return self.number

class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)
    schoolyear = models.ForeignKey(SchoolYear, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

class Student(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    klasses = models.ManyToManyField(
        Klass,
        through = 'StudentKlass'
    )
    characteristics = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['person__last_name', 'person__first_name']

    def __str__(self):
        return "%s %s %s" % (self.person.last_name, self.person.first_name, self.person.middle_name)

class Parrent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    relation_type = models.CharField(
        max_length=3,
        choices=ParrentType.choices,
        default=ParrentType.NONE,
    )

    class Meta:
        verbose_name = 'Родитель'
        verbose_name_plural = 'Родители'

    def __str__(self):
        return "%s %s %s" % (self.person.last_name, self.person.first_name, self.person.middle_name)

class StudentKlass(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    klass = models.ForeignKey(Klass, on_delete=models.CASCADE)
    date_from = models.DateField(auto_now_add=True)
    date_to = models.DateField()

    class Meta:
        ordering = ['-date_from']

    def __str__(self):
        return "%s %s %s" % (self.student.person.last_name, 
                            self.student.person.first_name, 
                            self.student.person.middle_name)

class StudentDocument(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="student_docs/%Y/%m%d/")
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    klass = models.ForeignKey(Klass, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, blank=True, null=True)
    lessons = models.ManyToManyField(Lesson, through='GroupLesson')

    def __str__(self):
        return self.name

class StudentGroup(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class GroupLesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

class GradeBook(models.Model):
    date = models.DateField(auto_now_add=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    schoolyear = models.ForeignKey(SchoolYear, on_delete=models.SET_NULL, blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_attended = models.BooleanField(default=True)
    grade = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    first_trimester = models.DecimalField(max_digits = 3, decimal_places = 2, blank=True, null=True)
    second_trimester = models.DecimalField(max_digits = 3, decimal_places = 2, blank=True, null=True)
    third_trimester = models.DecimalField(max_digits = 3, decimal_places = 2, blank=True, null=True)
    fourth_trimester = models.DecimalField(max_digits = 3, decimal_places = 2, blank=True, null=True)
    final_grade = models.DecimalField(max_digits = 3, decimal_places = 2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class LessonAttendance(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    schoolyear = models.ForeignKey(SchoolYear, on_delete=models.SET_NULL, blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_attended = models.BooleanField(default=True)
    reason = models.CharField(max_length=255, blank=True, null=True)
