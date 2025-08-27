from django.contrib import admin
from .models import *


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('username', 'mobile', 'first_name', 'last_name', 'clss')

    def save_model(self, request, obj, form, change):
        # اگر فیلد password در فرم عوض شده، آن را هش کن
        if "password" in form.changed_data:
            raw = form.cleaned_data.get("password")
            if raw:
                obj.set_password(raw)
        super().save_model(request, obj, form, change)

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
    list_display = ('username', 'get_full_name', 'clas')

    def save_model(self, request, obj, form, change):
        # اگر فیلد password در فرم عوض شده، آن را هش کن
        if "password" in form.changed_data:
            raw = form.cleaned_data.get("password")
            if raw:
                obj.set_password(raw)
        super().save_model(request, obj, form, change)

admin.site.register(Student, StudentAdmin)



@admin.register(Member)
class MemberModelAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "role")

    def save_model(self, request, obj, form, change):
        # اگر فیلد password در فرم عوض شده، آن را هش کن
        if "password" in form.changed_data:
            raw = form.cleaned_data.get("password")
            if raw:
                obj.set_password(raw)
        super().save_model(request, obj, form, change)

