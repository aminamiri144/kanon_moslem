# Generated by Django 4.2.7 on 2024-05-23 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_management', '0018_alter_disciplinegrade_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporttypes',
            name='grade',
            field=models.FloatField(default=0.0, verbose_name='نمره پیشفرض'),
        ),
    ]
