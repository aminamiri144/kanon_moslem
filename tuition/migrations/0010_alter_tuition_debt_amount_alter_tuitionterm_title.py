# Generated by Django 4.2.7 on 2024-09-01 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tuition', '0009_payday_sms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tuition',
            name='debt_amount',
            field=models.BigIntegerField(blank=True, default=None, null=True, verbose_name='میزان بدهی ترم'),
        ),
        migrations.AlterField(
            model_name='tuitionterm',
            name='title',
            field=models.CharField(default='دوره ...', max_length=255, verbose_name='عنوان(دوره)'),
        ),
    ]
