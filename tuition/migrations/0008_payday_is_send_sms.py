# Generated by Django 4.2.7 on 2024-08-29 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tuition', '0007_payday'),
    ]

    operations = [
        migrations.AddField(
            model_name='payday',
            name='is_send_sms',
            field=models.BooleanField(default=False, verbose_name='وضعیت اطلاع رسانی'),
        ),
    ]