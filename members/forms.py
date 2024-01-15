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
