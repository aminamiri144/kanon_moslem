from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth import logout
from . import titles
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse
from education_management.models import Class, Term
from django.shortcuts import render


class NoStudent(UserPassesTestMixin):
    def test_func(self):
        return not hasattr(self.request.user, 'student')

    def handle_no_permission(self):
        return redirect(reverse('spanel'))


class NoTeacher(UserPassesTestMixin):
    def test_func(self):
        return not hasattr(self.request.user, 'teacher')

    def handle_no_permission(self):
        return redirect(reverse('tpanel'))

    # class Index(TemplateView):


#     template_name = "landing/index.html"


class LoginRequiredMixin(object):
    """
    این کلاس در بررسی لاگین بودن یا نبودن
    کاربر کاربرد دارد.
    """
    login_required = True

    @classmethod
    def as_view(cls, **kwargs):
        self = cls()
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        if self.login_required:
            return login_required(view)
        else:
            return view


class SuccessMessageMixin:
    """
    Add a success message on successful form submission.
    """
    success_message = ''
    css = ''

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class UserLoginView(LoginView):
    """
    برای لاگین شدن کاربر استفاده میشود و
    از LoginView خود جانگو و فرم آن استفاده میکند

    """
    template_name = 'login.html'
    success_url = '/'

    def get_redirect_url(self):
        if 'term_title' not in self.request.session:
            default_term = Term.objects.filter(is_active=True).first()
            self.request.session['term_title'] = str(default_term)
            self.request.session['term_id'] = str(default_term.id)

        if hasattr(self.request.user, 'teacher'):
            return '/tpanel'

        if hasattr(self.request.user, 'student'):
            return '/spanel'

        return '/'


class PanelView(NoStudent, NoTeacher, LoginRequiredMixin, TemplateView):
    template_name = "panel.html"

    def get_context_data(self, **kwargs):
        context = {'page_title': titles.KANON_NAME, 'page_description': 'سامانه مدیریت کانون تربیتی',
                   'term': self.request.session['term_title'], 'classes': Class.objects.all()}
        return context


class StudentPanelView(LoginRequiredMixin, TemplateView):
    template_name = "spanel/student_panel.html"

    def get_context_data(self, **kwargs):
        context = {'page_title': titles.KANON_NAME, 'page_description': 'پنل کاربری متربی',
                   'term': self.request.session['term_title']}
        return context


class TeacherPanelView(LoginRequiredMixin, TemplateView, NoStudent):
    template_name = "teacher/panel.html"

    def get_context_data(self, **kwargs):
        clas_id = Class.objects.get(teacher=self.request.user).id
        context = {'page_title': titles.KANON_NAME, 'page_description': 'پنل کاربری مربی',
                   'term': self.request.session['term_title'], 'clas_id': clas_id}
        return context


class PanelView1(LoginRequiredMixin, TemplateView):
    template_name = "main1.html"

    def get_context_data(self, **kwargs):
        context = {'page_title': titles.KANON_NAME, 'page_description': 'سامانه مدیریت کانون تربیتی'}
        return context


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('/login')


class ChangeSystemTerm(LoginRequiredMixin, View):
    template_name = 'modals/change_term.html'

    def get(self, request):
        terms = Term.objects.all()
        return render(self.request, self.template_name, {"terms": terms})

    def post(self, request, *args, **kwargs):
        selected_term = request.POST.get('term_select')

        default_term = Term.objects.get(id=selected_term)
        self.request.session['term_title'] = str(default_term)
        self.request.session['term_id'] = str(default_term.id)
        messages.add_message(self.request, messages.SUCCESS, 'مدیریت ترم شما تغییر کرد')

        if hasattr(self.request.user, 'teacher'):
            return redirect(reverse('tpanel'))
        else:
            return redirect(reverse('panel'))
