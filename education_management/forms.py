from django import forms
from kanon_moslem.aminBaseViews import *
from kanon_moslem.datetimeUtils import change_date_to_english
from django.core.exceptions import ValidationError
from education_management.models import *



class TermCreateForm(BaseFormKanon):
    MODEL_VERBOSE_NAME = 'ترم تحصیلی'

    class Meta:
        model = Term
        fields = [
            "year",
            "mterm",
            "is_active",
        ]


class LessonCreateForm(BaseFormKanon):
    MODEL_VERBOSE_NAME = 'درس'

    class Meta:
        model = Lesson
        fields = [
            "title",
            "lesson_type",
            "description",
            "ratio",
        ]


class DisciplineGradeCreateForm(BaseFormKanon):
    MODEL_VERBOSE_NAME = 'مورد انضباطی'

    created = forms.CharField(label='تاریخ', widget=forms.TextInput(attrs={'placeholder': 'تاریخ را انتخاب کنید'}))

    def __init__(self, *args, **kwargs):
        super(DisciplineGradeCreateForm, self).__init__(*args, **kwargs)
        self.fields['student'].disabled = True
        self.fields['term'].disabled = True
    class Meta:
        model = DisciplineGrade
        fields = [
            "student",
            "discipline",
            "created",
            "grade",
            "term",
            "description",
        ]


    def clean_created(self):
        date = self.cleaned_data['created']
        try:
            date = change_date_to_english(date, 2)
        except:
            date = None
        return date