from django.db import models

from members.models import Student


class SendedSMS(models.Model):
    class Meta:
        verbose_name = "پیامک ارسالی"
        verbose_name_plural = "پیامک های ارسالی"

    SEND_TYPES = (
        ('shared', 'خدماتی'),
        ('simple', 'ساده'),
    )

    LAST_STATUS = (
        ('0', 'ارسال ناموفق(سایت)'),
        ('1', 'ارسال ناموفق(سامانه)'),
        ('2', 'ارسال موفق'),
        ('3', 'رسیده به مخاطب'),
        ('4', 'نرسیده به مخاطب'),
        ('5', 'ارسال شده(نتیجه نامشخص)'),
    )
    title = models.CharField(max_length=100, default="پیامک")
    to_number = models.CharField(max_length=11, verbose_name="شماره ارسالی")
    send_type = models.CharField(choices=SEND_TYPES, verbose_name='نوع ارسال', max_length=15, default='shared')
    pattern_id = models.IntegerField(verbose_name="کد پترن خدماتی", blank=True, null=True)
    last_status = models.CharField(max_length=100, verbose_name="پیغام آخرین وضعیت ارسال")
    params = models.CharField(max_length=255, null=True, blank=True)
    send_date = models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="متربی")
    recId = models.CharField(verbose_name='شناسه ارسالی پیامک', default='-1', max_length=64)


    def __str__(self):
        return f"به: {self.student} | شماره: {self.to_number} | وضعیت: {self.last_status} | توضیحات: {self.title}"


