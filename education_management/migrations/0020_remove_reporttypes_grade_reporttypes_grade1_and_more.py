# Generated by Django 4.2.7 on 2024-05-23 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_management', '0019_reporttypes_grade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reporttypes',
            name='grade',
        ),
        migrations.AddField(
            model_name='reporttypes',
            name='grade1',
            field=models.FloatField(default=0.0, verbose_name='نمره غیبت موجه'),
        ),
        migrations.AddField(
            model_name='reporttypes',
            name='grade2',
            field=models.FloatField(default=0.0, verbose_name='نمره غیبت غیر غیرموجه'),
        ),
        migrations.AddField(
            model_name='reporttypes',
            name='grade3',
            field=models.FloatField(default=0.0, verbose_name='نمره تاخیر موجه'),
        ),
        migrations.AddField(
            model_name='reporttypes',
            name='grade4',
            field=models.FloatField(default=0.0, verbose_name='نمره تاخیر غیر غیرموجه'),
        ),
    ]
