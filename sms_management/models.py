from django.db import models
from django_jalali.db import models as jmodels

from members.models import Student
from education_management.models import Term


class SendedSMS(models.Model):
    class Meta:
        verbose_name = "پیامک ارسالی"
        verbose_name_plural = "پیامک های ارسالی"

    SEND_TYPES = (
        ('shared', 'خدماتی'),
        ('simple', 'ساده'),
    )

    LAST_STATUS = (
        ('-10', 'در میان متغییر های ارسالی، لینک وجود دارد'),
        ('-7', 'خطایی در شماره فرستنده رخ داده است با پشتیبانی تماس بگیرید'),
        ('-6', 'خطای داخلی رخ داده است با پشتیبانی تماس بگیرید'),
        ('-5', 'متن ارسالی باتوجه به متغیرهای مشخص شده در متن پیشفرض همخوانی ندارد'),
        ('-4', 'کد متن ارسالی صحیح نمی‌باشد و یا توسط مدیر سامانه تأیید نشده است'),
        ('-3', 'خط ارسالی در سیستم تعریف نشده است، با پشتیبانی سامانه تماس بگیرید'),
        ('-2', 'محدودیت تعداد شماره، محدودیت هربار ارسال یک شماره موبایل می‌باشد'),
        ('-1', 'دسترسی برای استفاده از این وبسرویس غیرفعال است. با پشتیبانی تماس بگیرید'),
        ('0', 'نام کاربری یا رمزعبور صحیح نمی‌باشد'),
        ('2', 'اعتبار کافی نمی‌باشد'),
        ('6', 'سامانه درحال بروزرسانی می‌باشد'),
        ('7', 'متن حاوی کلمه فیلتر شده می‌باشد، با واحد اداری تماس بگیرید'),
        ('10', 'کاربر موردنظر فعال نمی‌باشد'),
        ('11', 'ارسال نشده'),
        ('12', 'مدارک کاربر کامل نمی‌باشد'),
        ('16', 'شماره گیرنده ای یافت نشد'),
        ('17', 'متن پیامک خالی می باشد'),
        ('35', 'شماره موبایل گیرنده در لیست سیاه مخابرات است'),
        ('success', 'ارسال موفق'),
    )
    title = models.CharField(max_length=100, default="پیامک")
    to_number = models.CharField(max_length=11, verbose_name="شماره ارسالی")
    send_type = models.CharField(choices=SEND_TYPES, verbose_name='نوع ارسال', max_length=15, default='shared')
    pattern_id = models.IntegerField(verbose_name="کد پترن خدماتی", blank=True, null=True)
    last_status = models.CharField(max_length=100, verbose_name="پیغام آخرین وضعیت ارسال")
    params = models.CharField(max_length=255, null=True, blank=True)
    send_date = jmodels.jDateTimeField(auto_now_add=True, verbose_name='زمان ارسال')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="متربی")
    recId = models.CharField(verbose_name='شناسه ارسالی پیامک', default='-1', max_length=64)
    tuition_term = models.ForeignKey('tuition.TuitionTerm', on_delete=models.CASCADE, verbose_name="شهریه ترم", null=True, blank=True)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, verbose_name="ترم", null=True, blank=True)


    @property
    def jd_send_date(self):
        """تاریخ ارسال به صورت شمسی"""
        try:
            return self.send_date.strftime('%Y/%m/%d %H:%M')
        except:
            return 'ثبت نشده!'

    @property
    def status_display(self):
        """نمایش وضعیت ارسال"""
        status_map = {
            '-10': 'در میان متغییر های ارسالی، لینک وجود دارد',
            '-7': 'خطایی در شماره فرستنده رخ داده است با پشتیبانی تماس بگیرید',
            '-6': 'خطای داخلی رخ داده است با پشتیبانی تماس بگیرید',
            '-5': 'متن ارسالی باتوجه به متغیرهای مشخص شده در متن پیشفرض همخوانی ندارد',
            '-4': 'کد متن ارسالی صحیح نمی‌باشد و یا توسط مدیر سامانه تأیید نشده است',
            '-3': 'خط ارسالی در سیستم تعریف نشده است، با پشتیبانی سامانه تماس بگیرید',
            '-2': 'محدودیت تعداد شماره، محدودیت هربار ارسال یک شماره موبایل می‌باشد',
            '-1': 'دسترسی برای استفاده از این وبسرویس غیرفعال است. با پشتیبانی تماس بگیرید',
            '0': 'نام کاربری یا رمزعبور صحیح نمی‌باشد',
            '2': 'اعتبار کافی نمی‌باشد',
            '6': 'سامانه درحال بروزرسانی می‌باشد',
            '7': 'متن حاوی کلمه فیلتر شده می‌باشد، با واحد اداری تماس بگیرید',
            '10': 'کاربر موردنظر فعال نمی‌باشد',
            '11': 'ارسال نشده',
            '12': 'مدارک کاربر کامل نمی‌باشد',
            '16': 'شماره گیرنده ای یافت نشد',
            '17': 'متن پیامک خالی می باشد',
            '35': 'شماره موبایل گیرنده در لیست سیاه مخابرات است',
            'success': 'ارسال موفق',
        }
        return status_map.get(self.last_status, self.last_status)

    @property
    def is_success(self):
        """آیا ارسال موفق بوده است؟"""
        return self.last_status == 'success'

    @property
    def is_error(self):
        """آیا ارسال با خطا مواجه شده است؟"""
        error_codes = ['-10', '-7', '-6', '-5', '-4', '-3', '-2', '-1', '0', '2', '6', '7', '10', '11', '12', '16', '17', '35']
        return self.last_status in error_codes

    def __str__(self):
        return f"به: {self.student} | شماره: {self.to_number} | وضعیت: {self.last_status} | توضیحات: {self.title}"


