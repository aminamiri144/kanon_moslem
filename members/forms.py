from django import forms
from members.models import *
from .validators import is_valid_codemeli
from django.core.exceptions import ValidationError
from kanon_moslem.datetimeUtils import change_date_to_english
from django.utils.html import format_html


class BaseFormKanon(forms.ModelForm):
    MODEL_VERBOSE_NAME = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = f'{field.label} {self.MODEL_VERBOSE_NAME}'

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = f'{visible.field.label} را وارد کنید ...'





class TeacherCreateForm(BaseFormKanon):
    MODEL_VERBOSE_NAME = 'سرگروه'

    birth_date = forms.DateField(label='تاریخ تولد')

    class Meta:
        model = Teacher
        fields = [
            "username",
            "first_name",
            "last_name",
            "mobile",
            "address",
            "password",
            "education",
            "clss",
            "experiences",
            "study_field",
        ]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not is_valid_codemeli(username):
            raise ValidationError("کدملی وارد شده معتبر نمی‌باشد")
        return username

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
            "father_name",
            "mather_name",
            "school_name"
        ]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not is_valid_codemeli(username):
            raise ValidationError("کدملی وارد شده معتبر نمی‌باشد")
        return username

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        try:
            birth_date = change_date_to_english(birth_date, 2)
        except:
            birth_date = None
        return birth_date
