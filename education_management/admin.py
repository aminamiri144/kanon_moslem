from django.contrib import admin
from .models import *


# Register your models here.

class TermAdmin(admin.ModelAdmin):
    list_display = ('get_full_title', 'is_active')


admin.site.register(Term, TermAdmin)


class LessonTypeAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(LessonType, LessonTypeAdmin)


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson_type', 'ratio')


admin.site.register(Lesson, LessonAdmin)


class SelectedLessonAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'term', 'grade')


admin.site.register(SelectedLesson, SelectedLessonAdmin)


class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Discipline, DisciplineAdmin)


class DisciplineGradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'discipline', 'grade', 'term', 'description', 'created')


admin.site.register(DisciplineGrade, DisciplineGradeAdmin)


class ControlSelectionAdmin(admin.ModelAdmin):
    list_display = ('clas', 'lesson', 'term')


admin.site.register(ControlSelection, ControlSelectionAdmin)


class GroupReportAdmin(admin.ModelAdmin):
    list_display = ('clas', 'report_type', 'title', 'date', 'term')


admin.site.register(GroupReport, GroupReportAdmin)


class ReportTypesAdmin(admin.ModelAdmin):
    list_display = ('title', 'grade1', 'grade2', 'grade3', 'grade4')


admin.site.register(ReportTypes, ReportTypesAdmin)
