from django.contrib import admin
from .models import *


class MemberAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'username', 'mobile')

admin.site.register(Member, MemberAdmin)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('username', 'mobile', 'first_name', 'last_name', 'clss')

admin.site.register(Teacher, TeacherAdmin)


class StudyFieldAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

admin.site.register(StudyField, StudyFieldAdmin)


class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

admin.site.register(Experience, ExperienceAdmin)


class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_year')

admin.site.register(Class, ClassAdmin)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'clas')

admin.site.register(Student, StudentAdmin)
