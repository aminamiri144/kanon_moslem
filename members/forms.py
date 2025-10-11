from django import forms
from members.models import *
from .validators import is_valid_codemeli
from django.core.exceptions import ValidationError
from kanon_moslem.datetimeUtils import change_date_to_english
from django.utils.html import format_html
from kanon_moslem.aminBaseViews import *




class TeacherCreateForm(BaseFormKanon):
    MODEL_VERBOSE_NAME = 'سرگروه'

    birth_date = forms.CharField(label='تاریخ تولد', widget=forms.TextInput(attrs={'placeholder': 'تاریخ را انتخاب کنید'}))

    class Meta:
        model = Teacher
        fields = [
            "username",
            "first_name",
            "last_name",
            "birth_date",
            "mobile",
            "address",
            "education",
            "clss",
            "experiences",
            "study_field",
        ]


    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        try:
            birth_date = change_date_to_english(birth_date, 2)
        except:
            birth_date = None
        return birth_date


class StudentCreateForm(BaseFormKanon):
    MODEL_VERBOSE_NAME = 'متربی'
    birth_date = forms.CharField(label='تاریخ تولد', widget=forms.TextInput(attrs={'placeholder': 'تاریخ را انتخاب کنید'}))

    class Meta:
        model = Student
        fields = [
            "first_name",
            "last_name",
            "username",
            "birth_date",
            "mobile",
            "address",
            "clas",
            "school_name",
            "father_name",
            "mather_name",
            "home_phone",
            "father_phone",
            "mather_phone"
        ]


    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        try:
            birth_date = change_date_to_english(birth_date, 2)
        except:
            birth_date = None
        return birth_date


class StudentUpdateForm(BaseFormKanon):
    MODEL_VERBOSE_NAME = 'متربی'
    birth_date = forms.CharField(
        label='تاریخ تولد', 
        widget=forms.TextInput(attrs={'placeholder': 'تاریخ را انتخاب کنید'}),
        required=False
    )
    
    # فیلدهای رمز عبور
    new_password = forms.CharField(
        label='رمز عبور جدید',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'رمز عبور جدید را وارد کنید',
            'class': 'form-control'
        }),
        required=False,
        help_text='برای تغییر رمز عبور، رمز جدید را وارد کنید. در غیر این صورت خالی بگذارید.'
    )
    
    confirm_password = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'رمز عبور را مجدداً وارد کنید',
            'class': 'form-control'
        }),
        required=False
    )

    class Meta:
        model = Student
        fields = [
            "first_name",
            "last_name",
            "username",
            "birth_date",
            "mobile",
            "address",
            "clas",
            "school_name",
            "father_name",
            "mather_name",
            "home_phone",
            "father_phone",
            "mather_phone"
        ]

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if not birth_date:
            return self.instance.birth_date
        try:
            birth_date = change_date_to_english(birth_date, 2)
        except:
            birth_date = self.instance.birth_date
        return birth_date

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password or confirm_password:
            if new_password != confirm_password:
                raise ValidationError({
                    'confirm_password': 'رمز عبور و تکرار آن یکسان نیستند.'
                })
            
            if new_password and len(new_password) < 5:
                raise ValidationError({
                    'new_password': 'رمز عبور باید حداقل 5 کاراکتر باشد.'
                })

        return cleaned_data