# Generated by Django 4.2.7 on 2023-12-23 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_alter_class_options_alter_experience_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='clas',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='members.class', verbose_name='گروه'),
        ),
    ]
