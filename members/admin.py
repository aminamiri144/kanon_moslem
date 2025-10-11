from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from .models import *


class TeacherAdminForm(forms.ModelForm):
    """فرم سفارشی برای ویرایش سرگروه در پنل ادمین"""
    password = forms.CharField(
        label='رمز عبور جدید',
        widget=forms.PasswordInput(attrs={'placeholder': 'برای تغییر رمز، رمز جدید را وارد کنید'}),
        required=False,
        help_text='برای تغییر رمز عبور، رمز جدید را وارد کنید. خالی بگذارید تا تغییری نکند.'
    )

    class Meta:
        model = Teacher
        fields = '__all__'

    def save(self, commit=True):
        teacher = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            teacher.set_password(password)
        if commit:
            teacher.save()
        return teacher


class TeacherAdmin(admin.ModelAdmin):
    form = TeacherAdminForm
    list_display = ('username', 'mobile', 'first_name', 'last_name', 'clss')
    fieldsets = (
        ('اطلاعات کاربری', {
            'fields': ('username', 'password', 'first_name', 'last_name', 'role')
        }),
        ('اطلاعات تماس', {
            'fields': ('mobile', 'address')
        }),
        ('اطلاعات تحصیلی', {
            'fields': ('education', 'clss', 'experiences', 'study_field')
        }),
        ('سایر اطلاعات', {
            'fields': ('birth_date', 'is_active', 'is_staff', 'is_superuser')
        }),
    )

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


class StudentAdminForm(forms.ModelForm):
    """فرم سفارشی برای ویرایش متربی در پنل ادمین"""
    password = forms.CharField(
        label='رمز عبور جدید',
        widget=forms.PasswordInput(attrs={'placeholder': 'برای تغییر رمز، رمز جدید را وارد کنید'}),
        required=False,
        help_text='برای تغییر رمز عبور، رمز جدید را وارد کنید. خالی بگذارید تا تغییری نکند.'
    )

    class Meta:
        model = Student
        fields = '__all__'

    def save(self, commit=True):
        student = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            student.set_password(password)
        if commit:
            student.save()
        return student


class StudentAdmin(admin.ModelAdmin):
    form = StudentAdminForm
    list_display = ('username', 'get_full_name', 'clas', 'account_balance_view')
    list_filter = ('clas', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'mobile')
    fieldsets = (
        ('اطلاعات کاربری', {
            'fields': ('username', 'password', 'first_name', 'last_name', 'role')
        }),
        ('اطلاعات تماس', {
            'fields': ('mobile', 'home_phone', 'address')
        }),
        ('اطلاعات خانوادگی', {
            'fields': ('father_name', 'mather_name', 'father_phone', 'mather_phone')
        }),
        ('اطلاعات تحصیلی', {
            'fields': ('clas', 'school_name', 'birth_date')
        }),
        ('اطلاعات مالی', {
            'fields': ('account_balance',),
            'classes': ('collapse',)
        }),
        ('دسترسی‌ها', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
            'classes': ('collapse',)
        }),
    )

admin.site.register(Student, StudentAdmin)



class MemberAdminForm(forms.ModelForm):
    """فرم سفارشی برای ویرایش کاربر در پنل ادمین"""
    password = forms.CharField(
        label='رمز عبور جدید',
        widget=forms.PasswordInput(attrs={'placeholder': 'برای تغییر رمز، رمز جدید را وارد کنید'}),
        required=False,
        help_text='برای تغییر رمز عبور، رمز جدید را وارد کنید. خالی بگذارید تا تغییری نکند.'
    )

    class Meta:
        model = Member
        fields = '__all__'

    def save(self, commit=True):
        member = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            member.set_password(password)
        if commit:
            member.save()
        return member


@admin.register(Member)
class MemberModelAdmin(admin.ModelAdmin):
    form = MemberAdminForm
    list_display = ("username", "first_name", "last_name", "role", "is_active")
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'mobile')
    fieldsets = (
        ('اطلاعات کاربری', {
            'fields': ('username', 'password', 'first_name', 'last_name', 'role')
        }),
        ('اطلاعات تماس', {
            'fields': ('mobile', 'address')
        }),
        ('سایر اطلاعات', {
            'fields': ('birth_date',)
        }),
        ('دسترسی‌ها و مجوزها', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
    )

