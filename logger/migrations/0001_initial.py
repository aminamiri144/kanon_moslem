# Generated by Django 4.2.7 on 2024-12-12 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Logger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('SMS', 'sms'), ('SYSTEM', 'system'), ('CELETY_MAIN', 'celery main'), ('CELERY_BEAT', 'celery beat')], default='SYSTEM', max_length=30)),
                ('text', models.TextField(blank=True, null=True)),
                ('decs', models.TextField(blank=True, null=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'گزارش',
                'verbose_name_plural': 'گزارش ها',
            },
        ),
    ]
