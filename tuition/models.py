from django.db import models

from education_management.models import Term
from members.models import Class, Student
from django_jalali.db import models as jmodels


# Create your models here.

class TuitionTerm(models.Model):
    class Meta:
        verbose_name = 'شهریه ترم'
        verbose_name_plural = "شهریه ترم ها"

    title = models.CharField(max_length=20, default="دوره ...", verbose_name="عنوان(دوره)")
    term = models.ForeignKey(Term, on_delete=models.CASCADE, verbose_name="ترم")
    price = models.BigIntegerField(verbose_name='مبلغ شهریه ترم', default=0)
    description = models.TextField(verbose_name='توضیحات', blank=True, null=True)
    groups = models.ManyToManyField(Class, verbose_name="گروه ها")

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
    is_paid = models.BooleanField(default=False, verbose_name="")
    debt_amount = models.BigIntegerField(verbose_name="میزان بدهی", default=None, blank=True, null=True)
    pay_day_1 = jmodels.jDateField(verbose_name="موعد پرداخت اول", blank=True, null=True)
    pay_day_2 = jmodels.jDateField(verbose_name="موعد پرداخت دوم", blank=True, null=True)
    pay_day_3 = jmodels.jDateField(verbose_name="موعد پرداخت سوم", blank=True, null=True)

    @property
    def jd_pay_day_1(self):
        pay_day_1 = str(self.pay_day_1).replace('-', '/')
        try:
            return pay_day_1
        except:
            return 'ثبت نشده!'

    @property
    def jd_pay_day_2(self):
        pay_day_2 = str(self.pay_day_2).replace('-', '/')
        try:
            return pay_day_2
        except:
            return 'ثبت نشده!'

    @property
    def jd_pay_day_3(self):
        pay_day_3 = str(self.pay_day_3).replace('-', '/')
        try:
            return pay_day_3
        except:
            return 'ثبت نشده!'

    @property
    def pay_status(self):
        if self.is_paid:
            return "شهریه کامل پرداخت شده"
        else:
            return "پرداخت نشده"
    @property
    def debt_amount_view(self):
        return "{:,}".format(self.debt_amount)

    def save(self, *args, **kwargs):
        if self.debt_amount is None:
            self.debt_amount = self.tuition_term.price
        if self.debt_amount <= 0:
            self.is_paid = True

        super(Tuition, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} | {self.debt_amount} | {self.pay_status}"


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

    def save(self, *args, **kwargs):
        tuition = Tuition.objects.get(student=self.student, term=self.term)
        tuition.debt_amount = tuition.debt_amount - self.amount
        tuition.save()
        super(Payment, self).save(*args, **kwargs)

    @property
    def jd_pay_date(self):
        pay_date = str(self.pay_date).replace('-', '/')
        try:
            return pay_date
        except:
            return 'ثبت نشده!'

    @property
    def amount_view(self):
        return "{:,}".format(self.amount)

    def __str__(self):
        return f"{self.student} | {self.amount} | {self.get_pay_type_display()} | {self.jd_pay_date}"
