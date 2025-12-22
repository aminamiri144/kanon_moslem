from django.db import models

from education_management.models import Term
from members.models import Class, Student
from django_jalali.db import models as jmodels

from sms_management.models import SendedSMS


class TuitionTerm(models.Model):
    class Meta:
        verbose_name = 'شهریه ترم'
        verbose_name_plural = "شهریه ترم ها"

    title = models.CharField(max_length=255, default="دوره ...", verbose_name="عنوان(دوره)")
    term = models.ForeignKey(Term, on_delete=models.CASCADE, verbose_name="ترم")
    price = models.BigIntegerField(verbose_name='مبلغ شهریه ترم', default=0)
    description = models.TextField(verbose_name='توضیحات', blank=True, null=True)
    groups = models.ManyToManyField(Class, verbose_name="گروه ها", blank=True, null=True)

    def __str__(self):
        return f"{self.title} | {self.price}"


class Tuition(models.Model):
    class Meta:
        verbose_name = 'شهریه متربی'
        verbose_name_plural = 'شهریه های متربی ها'
        constraints = [
            models.UniqueConstraint(fields=['student', 'term'], name='unique_tuition')
        ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='متربی')
    term = models.ForeignKey(Term, on_delete=models.CASCADE, verbose_name="ترم")
    tuition_term = models.ForeignKey(TuitionTerm, on_delete=models.CASCADE, verbose_name="شهریه مرجع")
    is_paid = models.BooleanField(default=False, verbose_name="وضعیت تسویه ترم")

    @property
    def pay_status(self):
        if self.is_paid:
            return "تسویه شده"
        else:
            return "بدهکار"

    def save(self, *args, **kwargs):
        from tuition.views import update_student_debt
        debt = update_student_debt(self.student)
        if debt <= 0:
            self.is_paid = True
        super(Tuition, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} | {self.student.account_balance} | {self.pay_status}"


class Payment(models.Model):
    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت ها"

    PAY_TYPES = (
        ('1', 'نقدی'),
        ('2', 'کارت به کارت'),
        ('3', 'چک'),
        ('4', 'تخفیف'),
        ('5', 'سایر'),
    )

    term = models.ForeignKey(Term, on_delete=models.CASCADE, verbose_name="ترم")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='متربی')
    amount = models.BigIntegerField(verbose_name="مبلغ پرداخت", default=0)
    pay_date = jmodels.jDateField(verbose_name="زمان پرداخت", blank=True, null=True)
    pay_type = models.CharField(choices=PAY_TYPES, verbose_name="نوع پرداخت", default="2", max_length=20)
    desc = models.CharField(max_length=200, verbose_name="توضیحات", blank=True, null=True)
    is_debt = models.BooleanField(default=False, verbose_name="بدهی")

    def save(self, *args, **kwargs):
        if self.desc is None:
            self.desc = 'ندارد'
        # اگر بدهی بود، amount را منفی می‌کنیم
        if self.is_debt:
            self.amount = -abs(self.amount)
        # اگر بستانکاری بود، amount را مثبت می‌کنیم
        elif not self.is_debt:
            self.amount = abs(self.amount)
        super(Payment, self).save(*args, **kwargs)
        from tuition.views import update_student_debt
        acc_balance = update_student_debt(self.student)
        student_tuition = Tuition.objects.get(student=self.student, term=self.term)
        if acc_balance <= 0 and not student_tuition.is_paid:
            student_tuition.is_paid = True
            student_tuition.save()

    @property
    def jd_pay_date(self):
        pay_date = str(self.pay_date).replace('-', '/')
        try:
            return pay_date
        except:
            return 'ثبت نشده!'

    @property
    def amount_view(self):
        return "{:,}".format(abs(self.amount))

    def __str__(self):
        return f"{self.student} | {self.amount} | {self.get_pay_type_display()} | {self.jd_pay_date}"


class PayDay(models.Model):
    class Meta:
        verbose_name = 'وعده پرداخت'
        verbose_name_plural = 'وعده های پرداخت'

    tuition = models.ForeignKey(Tuition, on_delete=models.CASCADE, verbose_name="شهریه")
    pay_date = jmodels.jDateField(verbose_name="تاریخ وعده")
    price = models.BigIntegerField(blank=True, null=True, verbose_name="مبلغ قابل پرداخت")
    is_paid = models.BooleanField(default=False, verbose_name="وضعیت پرداخت")
    is_send_sms = models.BooleanField(default=False, verbose_name="وضعیت اطلاع رسانی")
    sms = models.ForeignKey(SendedSMS, on_delete=models.DO_NOTHING, verbose_name="پیامک ارسالی", blank=True, null=True)

    @property
    def price_view(self):
        return "{:,}".format(self.price)

    @property
    def jd_pay_date(self):
        pay_date = str(self.pay_date).replace('-', '/')
        try:
            return pay_date
        except:
            return 'ثبت نشده!'

    def __str__(self):
        return f"{self.tuition.student.get_full_name()} | {self.jd_pay_date} | {self.is_paid}"
