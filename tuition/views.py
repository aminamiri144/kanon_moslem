import os
import jdatetime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, ListView, CreateView, UpdateView
from django.contrib import messages
from kanon_moslem.aminBaseViews import AminView, BaseCreateViewAmin
from kanon_moslem.views import NoStudent, LoginRequiredMixin, SuccessMessageMixin, NoTeacher
from sms_management.sms import SMS
from .forms import PaymentCreateForm, TuitionForm, PayDateCreateForm
from .models import *
from django.db.models import Q
from django.db.models import Sum


class TuitionMainView(AminView, ListView, LoginRequiredMixin, NoStudent):
    paginate_by = 20
    model = Tuition
    context_object_name = 'tuitions'
    template_name = "tuition/index.html"

    def get_queryset(self):
        value = self.request.GET.get('q', '')
        option = self.request.GET.get('option', '')
        term = Term.objects.get(id=int(self.request.session['term_id']))
        query = Q(**{f'{option}__icontains': value}) & Q(term=term)
        if value:
            object_list = self.model.objects.filter(query)
            self.request.session['search'] = self.request.GET.get('q', '')
        else:
            object_list = self.model.objects.filter(term=term)
        self.request.session['last_url'] = self.request.get_full_path()
        return object_list

    def get_initial(self):
        """
        در اینجا مقدار فیلد درخواست دهنده را با توجه به ادرس مقدار دهی میکنیم
        """
        if self.kwargs['option']:
            option = self.kwargs['option']
            return {'option': option}


class PaymentsOfStudentListView(View, NoStudent, LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        student = Student.objects.get(id=self.kwargs['pk'])
        payments = Payment.objects.filter(student=student)

        return render(self.request, 'tuition/list.html',
                      context={'payments': payments, 'student': student.get_full_name()})


class CreatePaymentView(LoginRequiredMixin, NoStudent, SuccessMessageMixin, CreateView):
    model = Payment
    template_name = "tuition/create_modal.html"
    form_class = PaymentCreateForm
    success_message = "پرداخت با موفقیت ثبت شد."

    def get_context_data(self, **kwargs):
        """در اینجا فیلد کاستومر یا درخواست دهنده را طوری تنظیم میکنیم که
        فقط درخواست دهنده ای که میخواهیم براش درخواست ثبت کنیم نمایش داده بشه
        و طوره نباشه که همه درخواست دهنده ها در اپشن های فیلد سلکت نمایش داده بشن
        """
        context = super(CreatePaymentView, self).get_context_data(**kwargs)
        context['form'].fields['student'].choices.field.queryset = Student.objects.filter(
            pk=self.kwargs['pk'])
        context['form'].fields['term'].choices.field.queryset = Term.objects.filter(
            id=int(self.request.session['term_id']))

        return context

    def get_initial(self):
        """
        در اینجا مقدار فیلد درخواست دهنده را با توجه به ادرس مقدار دهی میکنیم
        """
        student = self.kwargs['pk']
        return {'student': student, 'term': int(self.request.session['term_id'])}

    def get_success_url(self):
        return self.request.session['last_url']


class TuitionTermGenerate(AminView, LoginRequiredMixin, NoStudent, NoTeacher):
    def get(self, request, *args, **kwargs):
        form = TuitionForm()
        return render(request, template_name='tuition/generate_term_dore_tuition.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = TuitionForm(request.POST)
        if form.is_valid():
            tuition_amount = form.cleaned_data['tuition_amount']
            term = form.cleaned_data['term']
            dore = form.cleaned_data['dore']
            title = form.cleaned_data['title']
            desc = form.cleaned_data['desc']

            dore_class = Class.objects.filter(dore__exact=str(dore))
            if len(dore_class) == 0:
                messages.add_message(self.request, messages.WARNING, 'دوره انتخاب شده اشتباه است')

                return render(request, template_name='tuition/generate_term_dore_tuition.html', context={'form': form})

            if type(tuition_amount) != int:
                tuition_amount = int(tuition_amount)

            tt = TuitionTerm()
            tt.price = tuition_amount
            tt.title = title
            tt.description = desc
            tt.term = term
            tt.save()
            tt.groups.set(dore_class)

            for dc in dore_class:
                students = Student.objects.filter(clas=dc)

                for student in students:
                    ts = Tuition()
                    ts.student = student
                    ts.term = term
                    ts.tuition_term = tt
                    ts.save()
                    update_student_debt(student)
            messages.add_message(self.request, messages.SUCCESS,
                                 f'شهریه های متربیان دوره {dore} ترم {term} با موفقیت ایجاد شد.')
            return redirect('tuition-list')


class PayDateCreate(LoginRequiredMixin, NoStudent, SuccessMessageMixin, CreateView):
    model = PayDay
    template_name = "tuition/create_modal.html"
    form_class = PayDateCreateForm
    success_message = "موعد پرداخت با موفقیت ایجاد شد."

    def get_context_data(self, **kwargs):
        context = super(PayDateCreate, self).get_context_data(**kwargs)
        context['form'].fields['tuition'].choices.field.queryset = Tuition.objects.filter(
            pk=self.kwargs['pk'])
        return context

    def get_initial(self):
        tuition = self.kwargs['pk']
        return {'tuition': tuition}

    def get_success_url(self):
        return self.request.session['last_url']


class PayDayOfTuitionListView(LoginRequiredMixin, NoStudent, SuccessMessageMixin, AminView):
    def get(self, request, pk, *args, **kwargs):
        pds = PayDay.objects.filter(tuition__id=pk)
        student = Tuition.objects.get(id=pk).student
        context = {'pay_days': pds, 'student': student.get_full_name(),
                   'last_url': self.request.session.get('last_url', '')}
        return render(request, 'tuition/paydayslist.html', context=context)


def pay_day_payed_make_true(request, pk, *args, **kwargs):
    pd = PayDay.objects.get(id=pk)
    pd.is_paid = True
    pd.save()
    messages.add_message(request, messages.SUCCESS, 'پرداخت با موفقیت ثبت شد.')
    previous_url = request.META.get('HTTP_REFERER')
    return redirect(previous_url)


def update_student_debt(student):
    """بروزرسانی مانده حساب(بدهی/بسانکاری) کل متربی"""
    tuition_all = TuitionTerm.objects.filter(groups=student.clas)
    # مجموع کل شهریه های متربی
    total_debt = tuition_all.aggregate(total_debt=Sum('price'))['total_debt']

    payments = Payment.objects.filter(student=student)
    # مجموع کل پرداخت های متربی
    total_pay = payments.aggregate(total_pay=Sum('amount'))['total_pay']
    if total_pay is None:
        total_pay = 0
    account_balance = total_debt - total_pay
    student.account_balance = account_balance
    student.save()

    return account_balance


def update_students_debt_view(request):
    students = Student.objects.all()
    for student in students:
        update_student_debt(student)
    messages.add_message(request, messages.SUCCESS,
                         f'مانده حساب کل متربیان با موفقیت بروز شد!')
    return redirect(request.session['last_url'])