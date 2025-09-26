# Generated manually to fix timezone issue

from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sms_management', '0006_alter_sendedsms_send_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendedsms',
            name='send_date',
            field=models.DateTimeField(default=timezone.now, verbose_name='زمان ارسال'),
        ),
    ]
