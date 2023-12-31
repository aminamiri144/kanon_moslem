from django.db import models
from members.models import Student

# Create your models here.


class Term(models.Model):
    class Meta:
        verbose_name = "نیم‌سال تحصیلی"
        verbose_name_plural = "نیم‌سال‌های‌تحصیلی"
    TERM_CHOICES = [
        ('T', 'تابستان'),
        ('M', 'پاییز'),
        ('B', 'زمستان-بهار'),

    ]

    year = models.CharField(max_length=4, verbose_name="سال")
    mterm = models.CharField(choices=TERM_CHOICES, default='T',verbose_name="نیم‌سال", max_length=20)
    is_active = models.BooleanField(default=False, verbose_name="نیم‌سال فعال")

    def get_full_title(self):
        return f'{self.get_mterm_display()} | {self.year}'

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
    lesson_type = models.ForeignKey(LessonType, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name="نوع درس")
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
        ( '1' , 'عالی' ),
        ( '2' , 'بسیارخوب'),
        ( '3' , 'خوب'),
        ( '4' , 'متوسط'),
        ( '5' , 'ضعیف'),
        ( '6' , 'بسیارضعیف'),
        ( '7' , 'غایب'),
        ( '8' , 'ثبت‌نشده'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="متربی")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="درس")
    term = models.ForeignKey(Term, on_delete=models.CASCADE, verbose_name="ترم‌تحصیلی")
    grade = models.CharField(choices=GradeChoice, default='8' ,max_length=10, blank=True, null=True, verbose_name="نمره‌")

    unique_together = ('student', 'lesson','term',)

    def __str__(self):
        return self.student.get_full_name()


class Discipline(models.Model):
    class Meta:
        verbose_name = "مورد‌ انضباطی"
        verbose_name_plural = "موارد انضباطی"

    title = models.CharField(max_length=60, verbose_name="مورد انضباطی")

    def __str__(self):
        return self.title


class DisciplineGrade(models.Model):
    class Meta:
        verbose_name = "نمره انضباطی"
        verbose_name_plural = "نمرات انضباطی"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="متربی")
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, verbose_name="مورد انضباطی")
    created = models.DateTimeField(verbose_name="زمان ثبت")
    grade = models.IntegerField(verbose_name="نمره")
    term = models.ForeignKey(Term, on_delete=models.CASCADE, verbose_name="ترم‌تحصیلی")
    description = models.TextField(blank=True, null=True, verbose_name="توضیح")

    def __str__(self):
        return f"{self.student} | {self.discipline} | {self.created} | {self.grade}"





    


