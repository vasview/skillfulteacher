# Generated by Django 4.0.3 on 2022-05-15 12:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('people', '0001_initial'),
        ('staff', '0001_initial'),
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Unallocated', max_length=255)),
                ('klass', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='school.klass')),
            ],
            options={
                'verbose_name': 'Группы учеников',
                'verbose_name_plural': 'Список групп учеников',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.group')),
            ],
            options={
                'verbose_name': 'Состав группы учеников',
                'verbose_name_plural': 'Состав групп учеников',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('characteristics', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(through='student.GroupMember', to='student.group')),
            ],
            options={
                'verbose_name': 'Ученики',
                'verbose_name_plural': 'Список Учеников',
                'ordering': ['person__full_name'],
            },
        ),
        migrations.CreateModel(
            name='StudentKlass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField(auto_now_add=True)),
                ('date_to', models.DateField(blank=True, null=True)),
                ('klass', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='school.klass')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
            options={
                'verbose_name': 'Состав классов учеников',
                'verbose_name_plural': 'Составы классов учеников',
                'ordering': ['klass__code', 'student__person__full_name'],
            },
        ),
        migrations.CreateModel(
            name='StudentDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='student_docs/%Y/%m%d/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
            options={
                'verbose_name': 'Документы ученика',
                'verbose_name_plural': 'Список документов ученика',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='student',
            name='klasses',
            field=models.ManyToManyField(through='student.StudentKlass', to='school.klass'),
        ),
        migrations.AddField(
            model_name='student',
            name='person',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='people.person'),
        ),
        migrations.CreateModel(
            name='Parrent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation_type', models.CharField(choices=[('NA', 'Не выбрано'), ('MOM', 'Мама'), ('DAD', 'Папа'), ('CSD', 'Опекун')], default='NA', max_length=3)),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='people.person')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='student.student')),
            ],
            options={
                'verbose_name': 'Родители',
                'verbose_name_plural': 'Список Родителей',
                'ordering': ['person__full_name'],
            },
        ),
        migrations.CreateModel(
            name='LessonAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_attended', models.BooleanField(default=True)),
                ('reason', models.CharField(blank=True, max_length=255, null=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.lesson')),
                ('schoolyear', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.schoolyear')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
            options={
                'verbose_name': 'Табель посещамости учеников',
                'verbose_name_plural': 'Табеля посещамости учеников',
                'ordering': ['student__person__last_name', 'lesson__subject__name', 'date'],
            },
        ),
        migrations.AddField(
            model_name='groupmember',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student'),
        ),
        migrations.CreateModel(
            name='GroupLesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.group')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.lesson')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='lessons',
            field=models.ManyToManyField(through='student.GroupLesson', to='school.lesson'),
        ),
        migrations.AddField(
            model_name='group',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.subject'),
        ),
        migrations.AddField(
            model_name='group',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='staff.teacher'),
        ),
        migrations.CreateModel(
            name='GradeBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('grade', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('first_trimester', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('second_trimester', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('third_trimester', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('fourth_trimester', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('final_grade', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('schoolyear', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.schoolyear')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='student.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='school.subject')),
            ],
            options={
                'verbose_name': 'Дневник ученика',
                'verbose_name_plural': 'Дневники учеников',
                'ordering': ['student__person__last_name', 'subject__name'],
            },
        ),
    ]
