from members.models import *
from .forms import *
from kanon_moslem.aminBaseViews import *
from education_management.models import *
from kanon_moslem.views import *
from django.utils.datetime_safe import datetime

# Create your views here.


class TeacherCreateView(NoStudent, BaseCreateViewAmin):
    model = Teacher
    form_class = TeacherCreateForm
    success_message = 'سرگروه جدید با موفقیت افزوده شد !'
    PAGE_TITLE = 'افزودن سرگروه'
    ACTION_URL = 'teacher-add'
    BUTTON_TITLE = 'افزودن سرگروه'
    DATE_FIELD_ID = 'id_birth_date'
    SUCCESS_URL = 'teacher-detail'

    def form_valid(self, form):
        form.instance.role = "teacher"
        return super().form_valid(form)



class StudentCreateView(NoStudent, BaseCreateViewAmin):
    model = Student
    form_class = StudentCreateForm
    success_message = 'متربی جدید با موفقیت افزوده شد !'
    PAGE_TITLE = 'ثبت نام متربی'
    ACTION_URL = 'student-add'
    BUTTON_TITLE = "ثبت نام متربی"
    DATE_FIELD_ID = 'id_birth_date'
    SUCCESS_URL = 'student-detail'


class StudentDetailView(NoStudent, BaseDetailViewAmin):
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
        'home_phone',
        'father_phone',
        'mather_phone',
    ]
    models_property = ['register_date', 'birth_date']


class TeacherDetailView(NoStudent, BaseDetailViewAmin):
    PAGE_TITLE = 'مشخصات سرگروه'
    PAGE_DESCRIPTION = ''
    model = Teacher
    fields = [
        'first_name',
        'last_name',
        'mobile',
        'username',
        'birth_date',
        'clss',
        'experiences',
        'study_field',
        'address',
    ]
    models_property = ['birth_date']


class StudentListView(AminView, NoStudent, LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Student
    context_object_name = 'students'
    template_name = 'student/list.html'

    def get_paginate_by(self, queryset):
        per_page = self.request.GET.get('per_page')
        return int(per_page) if per_page and per_page.isdigit() else 10  # مقدار پیش‌فرض ۱۰

    def get_queryset(self):
        value = self.request.GET.get('q', '')
        option = self.request.GET.get('option', '')
        query = {f'{option}__icontains': value}
        if value:
            if hasattr(self.request.user, 'teacher'):
                t_id = self.request.user.id
                teacher = Teacher.objects.get(id=t_id)
                tc = teacher.clss
                object_list = self.model.objects.filter(**query, clas=tc, is_active=True)
            else:
                object_list = self.model.objects.filter(**query, is_active=True)

            self.request.session['search'] = self.request.GET.get('q', '')
        else:
            if hasattr(self.request.user, 'teacher'):
                t_id = self.request.user.id
                teacher = Teacher.objects.get(id=t_id)
                tc = teacher.clss
                object_list = self.model.objects.filter(clas_id=tc.id, is_active=True)
                self.template_name = 'teacher/student_list_4teacher.html'
            else:
                object_list = self.model.objects.filter(is_active=True)
        return object_list

    def get_initial(self):
        """
        در اینجا مقدار فیلد درخواست دهنده را با توجه به ادرس مقدار دهی میکنیم 
        """
        if self.kwargs['option']:
            option = self.kwargs['option']
            return {'option': option}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        params = self.request.GET.copy()
        params.pop('page', None)  # حذف page قبلی
        ctx['querystring'] = params.urlencode()  # مثل: q=...&option=...
        return ctx


class StudentUpdateView(NoStudent, LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentCreateForm
    template_name = "student/student_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['term'] = self.request.session['term_title']
        context['action_url'] = reverse(
            'student-update', kwargs={'pk': self.object.pk, })

        return context

    def form_valid(self, form):
        birth_date_str = self.request.POST.get('birth_date')
        if '-' in birth_date_str:
            form.instance.birth_date = birth_date_str
        else:
            form.instance.birth_date = birth_date_str.replace('/', '-')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('student-detail', kwargs={'pk': self.object.pk, })
