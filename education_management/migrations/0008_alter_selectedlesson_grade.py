# Generated by Django 4.2.7 on 2024-01-30 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_management', '0007_alter_controlselection_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selectedlesson',
            name='grade',
            field=models.CharField(blank=True, choices=[('5', 'عالی'), ('4', 'بسیارخوب'), ('3', 'خوب'), ('2', 'متوسط'), ('1', 'ضعیف'), ('0', 'بسیارضعیف'), ('g', 'غایب'), ('n', 'ثبت\u200cنشده')], default='n', max_length=10, null=True, verbose_name='نمره\u200c'),
        ),
    ]
