# Generated by Django 4.2.7 on 2023-11-26 09:01

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='نام گروه')),
                ('created_year', models.CharField(max_length=4, verbose_name='سال تشکیل')),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='StudyField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='تاریخ تولد'),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('member_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('education', models.CharField(blank=True, max_length=100, verbose_name='تحصیلات')),
                ('clss', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='members.class', verbose_name='گروه')),
                ('experiences', models.ManyToManyField(to='members.experience', verbose_name='تخصص ها')),
                ('study_field', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='members.studyfield', verbose_name='رشته تحصیلی')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('members.member',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='experience',
            name='teachers',
            field=models.ManyToManyField(to='members.teacher'),
        ),
    ]
