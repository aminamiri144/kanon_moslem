from django.shortcuts import render
from members.models import *
from django.views.generic.edit import CreateView
from kanon_moslem.views import LoginRequiredMixin, SuccessMessageMixin
from .forms import *
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager

# Create your views here.


class BaseCreateViewKanon(LoginRequiredMixin, SuccessMessageMixin):
    PAGE_TITLE = ''
    PAGE_DESCRIPTION = ''
    ACTION_URL = ''
    BUTTON_TITLE = ''
    ACTION_URL = 'panel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.PAGE_TITLE
        context['page_description'] = self.PAGE_DESCRIPTION
        context['action_url'] = reverse(self.ACTION_URL)
        context['button_title'] = self.BUTTON_TITLE
        return context
    
    def get_success_url(self):
        return reverse(self.ACTION_URL, kwargs={'pk': self.object.pk, })



class TeacherCreateView(BaseCreateViewKanon, CreateView):
    model = Teacher
    template_name = 'members/member_add.html'
    form_class = TeacherCreateForm
    success_message = 'کاربر جدید با موفقیت افزوده شد !'
    PAGE_TITLE = 'افزودن سرگروه'
    ACTION_URL = 'teacher-add'
    BUTTON_TITLE = 'افزودن سرگروه'


    

class StudentCreateView(BaseCreateViewKanon, CreateView):
    model = Student
    template_name = 'members/member_add.html'
    form_class = StudentCreateForm
    success_message = 'کاربر جدید با موفقیت افزوده شد !'
    PAGE_TITLE = 'ثبت نام متربی'
    ACTION_URL = 'student-add'
    BUTTON_TITLE = "ثبت نام متربی"

    def form_valid(self, form):
        form.instance.password = make_password('12345')
        form.instance.email = 'test@example.com'
        return super().form_valid(form)
    
