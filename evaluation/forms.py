from django import forms
from members.models import Class
from education_management.models import Lesson, Term

class LessonClassSelectionForm(forms.Form):
    clas = forms.ModelChoiceField(queryset=Class.objects.all(), label='انتخاب گروه:')
    lesson = forms.ModelChoiceField(queryset=Lesson.objects.all(), label='انتخاب درس:')
    term_id = forms.CharField(required=True, label='ترم: (ترم فعال سامانه)')



    def __init__(self, *args, **kwargs):
        super(LessonClassSelectionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        self.fields['term_id'].initial = Term.objects.filter(is_active=True).first()
        self.fields['term_id'].disabled = True