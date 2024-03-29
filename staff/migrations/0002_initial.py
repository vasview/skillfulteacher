# Generated by Django 4.0.3 on 2022-05-31 20:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('school', '0002_initial'),
        ('student', '0001_initial'),
        ('staff', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherstudent',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student'),
        ),
        migrations.AddField(
            model_name='teacherstudent',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.teacher'),
        ),
        migrations.AddField(
            model_name='teacherdocument',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.teacher'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='job_positions',
            field=models.ManyToManyField(through='staff.JobPositionChange', to='staff.jobposition'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='klasses',
            field=models.ManyToManyField(through='school.ClassroomTeacher', to='school.klass'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jobpositionchange',
            name='job_position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.jobposition'),
        ),
        migrations.AddField(
            model_name='jobpositionchange',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.teacher'),
        ),
    ]
