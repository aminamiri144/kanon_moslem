# Generated manually to fix timezone issue

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms_management', '0005_sendedsms_term_sendedsms_tuition_term_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendedsms',
            name='send_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال'),
        ),
    ]