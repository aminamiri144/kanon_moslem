from django.shortcuts import render
from members.models import Member, Teacher
from django.views.generic.edit import CreateView
from kanon_moslem.views import LoginRequiredMixin, SuccessMessageMixin
from .forms import TeacherCreateForm
from django.urls import reverse
# Create your views here.



class TeacherCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Teacher
    template_name = 'create_member.html'
    form_class = TeacherCreateForm
    success_message = 'کاربر جدید با موفقیت افزوده شد !'
    
    def get_success_url(self):
        return reverse('member-detail', kwargs={'pk': self.object.pk,})
