from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import *
from django.core.exceptions import ValidationError
from django_jalali.db import models as jmodels
from jdatetime import datetime as jdatetime


# Create your models here.


class Class(models.Model):
    class Meta:
        verbose_name = "گروه"
        verbose_name_plural = "گروه ها"

    name = models.CharField(max_length=100, verbose_name="نام گروه")
    created_year = models.CharField(max_length=4, verbose_name="سال تشکیل")
    dore = models.CharField(max_length=2, verbose_name="دوره", default="0")

    def __str__(self):
        return self.name


class Experience(models.Model):
    class Meta:
        verbose_name = "تخصص"
        verbose_name_plural = "تخصص ها"

    title = models.CharField(max_length=100, verbose_name="عنوان تخصص")
    description = models.TextField(verbose_name="توضیحات", blank=True, null=True)

    def __str__(self):
        return self.title


class StudyField(models.Model):
    class Meta:
        verbose_name = "رشته تحصیلی"
        verbose_name_plural = "رشته های تحصیلی"

    title = models.CharField(max_length=100, verbose_name="عنوان رشته")
    description = models.TextField(verbose_name="توضیحات", blank=True, null=True)

    def __str__(self):
        return self.title


class Member(AbstractUser):
    mobile_validator = UnicodeIranMobileValidator()

    username = models.CharField(max_length=10, blank=True, verbose_name="کد ملی",
                                unique=True,
                                error_messages={
                                    "unique": "این کد ملی قبلا ثبت شده است .",
                                }
                                )

    mobile = models.CharField(
        max_length=11, blank=True,
        verbose_name="موبایل",
        validators=[mobile_validator],
    )
    address = models.CharField(max_length=250, blank=True, verbose_name="آدرس منزل")

    birth_date = jmodels.jDateField(verbose_name="تاریخ تولد", blank=True, null=True)

    @property
    def jd_birth_date(self):
        birth_date = str(self.birth_date).replace('-', '/')
        try:
            return birth_date
        except:
            return 'ثبت نشده!'

    # def clean(self):
    #     #super().clean()
    #     if not is_valid_codemeli(self.username):
    #         raise ValidationError("کدملی وارد شده معتبر نمی‌باشد")


    def __str__(self):
        return self.get_full_name()


class Teacher(Member):
    # objects = jmodels.jManager()
    class Meta:
        verbose_name = "سرگروه"
        verbose_name_plural = "سرگروه ها"

    EDUCATION_CHOICES = [
        ('DA', 'متوسطه'),
        ('KD', 'کاردانی'),
        ('KA', 'کارشناسی'),
        ('KAA', 'کارشناسی ارشد'),
        ('DC', 'دکتری'),
        ('HZ', 'حوزوی'),
        ('OT', 'سایر'),
    ]

    education = models.CharField(choices=EDUCATION_CHOICES, default='OT', verbose_name="تحصیلات", max_length=100,
                                 blank=True, null=True)
    clss = models.ForeignKey(Class, on_delete=models.DO_NOTHING, verbose_name="گروه", blank=True, null=True)
    experiences = models.ManyToManyField(Experience, verbose_name="تخصص ها", blank=True, null=True)
    study_field = models.ForeignKey(StudyField, on_delete=models.DO_NOTHING, verbose_name="رشته تحصیلی", blank=True,
                                    null=True)

    def __str__(self):
        return self.get_full_name()


class Student(Member):
    # objects = jmodels.jManager()
    class Meta:
        verbose_name = "متربی"
        verbose_name_plural = "متربیان"

    clas = models.ForeignKey(Class, on_delete=models.DO_NOTHING, verbose_name="گروه")
    father_name = models.CharField(max_length=30, verbose_name="نام پدر ")
    mather_name = models.CharField(max_length=30, verbose_name="نام و نام خانوادگی مادر")
    register_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت نام")
    school_name = models.CharField(max_length=50, verbose_name="نام مدرسه ", blank=True, null=True)
    home_phone = models.CharField(max_length=11, verbose_name="تلفن منزل", blank=True, null=True)
    father_phone = models.CharField(max_length=11, verbose_name="شماره موبایل پدر", blank=True, null=True)
    mather_phone = models.CharField(max_length=11, verbose_name="شماره موبایل مادر", blank=True, null=True)
    account_balance = models.BigIntegerField(verbose_name="مانده حساب کل", default=0)

    @property
    def jd_register_date(self):
        jd_reg_date = str(self.register_date).replace('-', '/')
        try:
            return jd_reg_date
        except:
            return 'ثبت نشده!'

    @property
    def account_balance_view(self):
        balance = "{:,}".format(self.account_balance)

        if self.account_balance < 0:
            ac = self.account_balance * -1
            ac = "{:,}".format(ac)
            balance = f" {ac} تومان (بستانکار)"
        return balance

    def __str__(self):
        return self.get_full_name()
