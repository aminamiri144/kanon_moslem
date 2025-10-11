from members.models import *
from .forms import *
from kanon_moslem.aminBaseViews import *
from education_management.models import *
from kanon_moslem.views import *
from django.utils.datetime_safe import datetime
from django.contrib import messages
from django.shortcuts import render, get_object_or_404

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



class StudentCreateView(NoStudent, LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentCreateForm
    template_name = 'student/student_create.html'
    success_message = 'متربی جدید با موفقیت افزوده شد!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'ثبت نام متربی جدید'
        context['page_description'] = 'فرم ثبت نام و ایجاد متربی جدید در سیستم'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if not self.object.pk or not self.object.has_usable_password():
            self.object.set_password("12345")
        self.object.role = 'student'
        self.object.save()
        form.save_m2m()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('student-detail', kwargs={'pk': self.object.pk})


class StudentDetailView(NoStudent, LoginRequiredMixin, View):
    template_name = 'student/student_detail.html'

    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        context = {
            'student': student,
            'page_title': 'مشخصات متربی',
            'page_description': 'اطلاعات کامل متربی'
        }
        return render(request, self.template_name, context)


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
    form_class = StudentUpdateForm
    template_name = "student/student_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['term'] = self.request.session['term_title']
        context['action_url'] = reverse(
            'student-update', kwargs={'pk': self.object.pk, })
        context['student'] = self.object

        return context

    def form_valid(self, form):
        birth_date_str = self.request.POST.get('birth_date')
        if birth_date_str:
            if '-' in birth_date_str:
                form.instance.birth_date = birth_date_str
            else:
                form.instance.birth_date = birth_date_str.replace('/', '-')
        
        # بررسی تغییر رمز عبور
        new_password = form.cleaned_data.get('new_password')
        if new_password:
            form.instance.set_password(new_password)
            messages.success(self.request, 'رمز عبور با موفقیت تغییر کرد.')
        
        messages.success(self.request, 'اطلاعات متربی با موفقیت ویرایش شد.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('student-detail', kwargs={'pk': self.object.pk, })
