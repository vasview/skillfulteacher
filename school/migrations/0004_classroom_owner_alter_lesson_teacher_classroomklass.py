# Generated by Django 4.0.3 on 2022-06-12 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_alter_jobpositionchange_options_and_more'),
        ('school', '0003_alter_classroomteacher_klass_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rooms', to='staff.teacher'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lessons', to='staff.teacher'),
        ),
        migrations.CreateModel(
            name='ClassRoomKlass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateTimeField()),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='klasses', to='school.classroom')),
                ('klass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classrooms', to='school.klass')),
            ],
            options={
                'verbose_name': 'Классный кабинет',
                'verbose_name_plural': 'Классные кабинеты',
            },
        ),
    ]
