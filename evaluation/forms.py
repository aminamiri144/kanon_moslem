from django import forms
from members.models import Class
from education_management.models import Lesson, Term


class LessonClassSelectionForm(forms.Form):
    clas = forms.ModelChoiceField(queryset=Class.objects.all(), label='انتخاب گروه:')
    lesson = forms.ModelChoiceField(queryset=Lesson.objects.all(), label='انتخاب درس:')

    def __init__(self, *args, **kwargs):
        super(LessonClassSelectionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

