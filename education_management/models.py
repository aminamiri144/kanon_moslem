from django.db import models
from members.models import Student, Class
from django_jalali.db import models as jmodels
import jdatetime


# Create your models here.


class Term(models.Model):
    class Meta:
        verbose_name = "نیم‌سال تحصیلی"
        verbose_name_plural = "نیم‌سال‌های‌تحصیلی"

        constraints = [
            models.UniqueConstraint(fields=['year', 'mterm'], name='unique_term')
        ]

    TERM_CHOICES = [
        ('T', 'تابستان'),
        ('M', 'پاییز'),
        ('B', 'زمستان-بهار'),

    ]

    year = models.CharField(max_length=4, verbose_name="سال")
    mterm = models.CharField(choices=TERM_CHOICES, default='T', verbose_name="نیم‌سال", max_length=20)
    is_active = models.BooleanField(default=False, verbose_name="نیم‌سال فعال")

    unique_together = ('year', 'mterm',)

    @property
    def get_full_title(self):
        return f'{self.get_mterm_display()} | {self.year}'

    @property
    def get_is_active(self):
        if self.is_active == False:
            return '0'
        else:
            return '1'

    def __str__(self):
        return f'{self.get_mterm_display()} | {self.year}'


# class EduTerm(models.Model):
#     title = models.CharField(max_length=50, 
class LessonType(models.Model):
    class Meta:
        verbose_name = "نوع درس"
        verbose_name_plural = "انواع درس"

    title = models.CharField(max_length=50, verbose_name="نوع درس")

    def __str__(self):
        return self.title


class Lesson(models.Model):
    class Meta:
        verbose_name = "درس"
        verbose_name_plural = "درس‌ها"

    title = models.CharField(max_length=50, verbose_name="نام درس")
    lesson_type = models.ForeignKey(LessonType, on_delete=models.DO_NOTHING, blank=True, null=True,
                                    verbose_name="نوع درس")
    description = models.TextField(max_length=300, verbose_name="توضیحات درس", null=True, blank=True)
    ratio = models.IntegerField(default=1, verbose_name="ضریب درس")

    def __str__(self):
        return self.title


class SelectedLesson(models.Model):
    class Meta:
        verbose_name = "درس گرفته‌شده"
        verbose_name_plural = "درس‌های گرفته‌شده"

        constraints = [
            models.UniqueConstraint(fields=['student', 'lesson', 'term'], name='unique_student_term_lesson')
        ]

    GradeChoice = [
        ('5', 'عالی'),
        ('4', 'بسیارخوب'),
        ('3', 'خوب'),
        ('2', 'متوسط'),
        ('1', 'ضعیف'),
        ('0', 'بسیارضعیف'),
        ('g', 'غایب'),
        ('n', 'ثبت‌نشده'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="متربی")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="درس")
    term = models.ForeignKey(Term, on_delete=models.CASCADE, verbose_name="ترم‌تحصیلی")
    grade = models.CharField(choices=GradeChoice, default='n', max_length=10, blank=True, null=True,
                             verbose_name="نمره‌")
    description = models.CharField(blank=True, null=True, verbose_name="توضیحات", default="توضیحات", max_length=255)

    unique_together = ('student', 'lesson', 'term',)

    def __str__(self):
        return self.student.get_full_name()


class Discipline(models.Model):
    class Meta:
        verbose_name = "مورد‌ انضباطی"
        verbose_name_plural = "موارد انضباطی"

    title = models.CharField(max_length=60, verbose_name="مورد انضباطی")

    def __str__(self):
        return self.title


class ControlSelection(models.Model):
    class Meta:
        verbose_name = "کنترل انتخاب واحد گروه"
        verbose_name_plural = "کنترل انتخاب واحد گروه ها"

        constraints = [
            models.UniqueConstraint(fields=['clas', 'lesson', 'term'], name='unique_clas_term_lesson')
        ]

    clas = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name="گروه")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="درس")
    term = models.ForeignKey(Term, on_delete=models.CASCADE, verbose_name="ترم‌تحصیلی")

    unique_together = ('clas', 'lesson', 'term',)

    def __str__(self):
        return f"{self.clas} | {self.lesson} | {self.term}"


class ReportTypes(models.Model):
    class Meta:
        verbose_name = 'نوع گزارش'
        verbose_name_plural = 'انواع گزارش'

    title = models.CharField(max_length=60, verbose_name="نوع گزارش")

    def __str__(self):
        return self.title


class GroupReport(models.Model):
    class Meta:
        verbose_name = "گزارش روزانه گروه"
        verbose_name_plural = "گزارش های روزانه گروه ها"

        constraints = [
            models.UniqueConstraint(fields=['clas', 'term', 'date', 'report_type'],
                                    name='unique_clas_term_date_report_type')
        ]

    title = models.CharField(max_length=60, default="برگزاری گروه", verbose_name="عنوان گزارش")
    report_type = models.ForeignKey(ReportTypes, on_delete=models.CASCADE, verbose_name="نوع گزارش", default=1)
    clas = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name="گروه")
    term = models.ForeignKey(Term, on_delete=models.CASCADE, verbose_name="ترم‌تحصیلی")
    date = jmodels.jDateField(verbose_name="تاریخ گزارش")

    unique_together = ('clas', 'term', 'date', 'report_type',)

    @property
    def jd_date(self):
        date = str(self.date).replace('-', '/')
        try:
            return date
        except:
            return 'ثبت نشده!'

    def __str__(self):
        return f"{self.clas} | {self.report_type} | {self.title}"


class DisciplineGrade(models.Model):
    class Meta:
        verbose_name = "نمره انضباطی"
        verbose_name_plural = "نمرات انضباطی"

    report = models.ForeignKey(GroupReport, on_delete=models.CASCADE, verbose_name="گزارش گروه", blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="متربی")
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, verbose_name="مورد انضباطی")
    created = jmodels.jDateField(verbose_name="زمان ثبت")
    grade = models.IntegerField(verbose_name="نمره")
    term = models.ForeignKey(Term, on_delete=models.CASCADE, verbose_name="ترم‌تحصیلی")
    description = models.TextField(blank=True, null=True, verbose_name="توضیح")

    @property
    def jd_created_date(self):
        created_date = str(self.created).replace('-', '/')
        try:
            return created_date
        except:
            return 'ثبت نشده!'

    def __str__(self):
        return f"{self.student} | {self.discipline} | {self.created} | {self.grade}"
