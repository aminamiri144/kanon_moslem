# Generated by Django 4.2.7 on 2024-03-04 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('education_management', '0013_groupreport_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, verbose_name='نوع گزارش')),
            ],
            options={
                'verbose_name': 'نوع گزارش',
                'verbose_name_plural': 'انواع گزارش',
            },
        ),
        migrations.AlterField(
            model_name='groupreport',
            name='title',
            field=models.CharField(default='برگزاری گروه', max_length=60, verbose_name='عنوان گزارش'),
        ),
        migrations.AlterField(
            model_name='groupreport',
            name='report_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education_management.reporttypes', verbose_name='نوع گزارش'),
        ),
    ]