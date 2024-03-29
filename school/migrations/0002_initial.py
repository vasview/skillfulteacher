# Generated by Django 4.0.3 on 2022-05-31 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('staff', '0001_initial'),
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachersubject',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.teacher'),
        ),
        migrations.AddField(
            model_name='subject',
            name='teachers',
            field=models.ManyToManyField(through='school.TeacherSubject', to='staff.teacher'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='classroom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.classroom'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='schoolyear',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.schoolyear'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.subject'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='staff.teacher'),
        ),
        migrations.AddField(
            model_name='klasshistory',
            name='classroom_teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='staff.teacher'),
        ),
        migrations.AddField(
            model_name='klasshistory',
            name='klass',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='school.klass'),
        ),
        migrations.AddField(
            model_name='klasshistory',
            name='school_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.schoollevel'),
        ),
        migrations.AddField(
            model_name='klasshistory',
            name='school_year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.schoolyear'),
        ),
        migrations.AddField(
            model_name='klass',
            name='school_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.schoollevel'),
        ),
        migrations.AddField(
            model_name='klass',
            name='school_year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.schoolyear'),
        ),
        migrations.AddField(
            model_name='classroomteacher',
            name='klass',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.klass'),
        ),
        migrations.AddField(
            model_name='classroomteacher',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='staff.teacher'),
        ),
    ]
