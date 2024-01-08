from members.models import *
from .forms import *
from kanon_moslem.aminBaseViews import *


# Create your views here.


class TeacherCreateView(BaseCreateViewKanon):
    model = Teacher
    form_class = TeacherCreateForm
    success_message = 'سرگروه جدید با موفقیت افزوده شد !'
    PAGE_TITLE = 'افزودن سرگروه'
    ACTION_URL = 'teacher-add'
    BUTTON_TITLE = 'افزودن سرگروه'


    

class StudentCreateView(BaseCreateViewKanon):
    model = Student
    form_class = StudentCreateForm
    success_message = 'متربی جدید با موفقیت افزوده شد !'
    PAGE_TITLE = 'ثبت نام متربی'
    ACTION_URL = 'student-add'
    BUTTON_TITLE = "ثبت نام متربی"

    


class StudentDetailView(BaseDetailView):
    PAGE_TITLE = 'مشخصات متربی'
    PAGE_DESCRIPTION = ''
    model = Student
    fields = [
        'first_name',
        'last_name',
        'username',
        'mobile',
        'address',
        'clas',
        'school_name',
        'father_name',
        'mather_name', 
        'register_date',
        'birth_date', 
    ]
    models_property = ['register_date','birth_date']
