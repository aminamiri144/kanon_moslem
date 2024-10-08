# Generated by Django 4.2.7 on 2024-08-26 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_management', '0002_sendedsms_recid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendedsms',
            name='last_status',
            field=models.CharField(max_length=100, verbose_name='پیغام آخرین وضعیت ارسال'),
        ),
        migrations.AlterField(
            model_name='sendedsms',
            name='recId',
            field=models.IntegerField(default=0, verbose_name='شناسه ارسالی پیامک'),
        ),
    ]
