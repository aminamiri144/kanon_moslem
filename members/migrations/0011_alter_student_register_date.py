# Generated by Django 4.2.7 on 2024-01-16 15:34

import datetime
from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0010_alter_member_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='register_date',
            field=django_jalali.db.models.jDateTimeField(default=datetime.datetime(2024, 1, 16, 19, 4, 7, 132515), verbose_name='تاریخ ثبت نام'),
        ),
    ]
