# Generated by Django 4.2.7 on 2024-01-30 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_management', '0008_alter_selectedlesson_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='selectedlesson',
            name='description',
            field=models.TextField(blank=True, default='توضیحات', null=True, verbose_name='توضیحات'),
        ),
    ]
