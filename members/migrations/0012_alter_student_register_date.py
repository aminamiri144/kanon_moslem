# Generated by Django 4.2.7 on 2024-01-16 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0011_alter_student_register_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='register_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت نام'),
        ),
    ]
