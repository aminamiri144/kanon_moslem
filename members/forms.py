from django import forms
from members.models import Member, Teacher
from .validators import is_valid_codemeli
from django.core.exceptions import ValidationError



class TeacherCreateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields= [
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
    
    def __init__(self, *args, **kwargs):
        super(TeacherCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not is_valid_codemeli(username):
            raise ValidationError("کدملی وارد شده معتبر نمی‌باشد")
        return username