# Generated by Django 4.2.7 on 2024-05-23 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_management', '0017_disciplinegrade_report_alter_groupreport_report_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disciplinegrade',
            name='grade',
            field=models.FloatField(verbose_name='نمره'),
        ),
    ]
