import os
import jdatetime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, ListView, CreateView, UpdateView
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
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
        query = Q(**{f'{option}__icontains': value}) & Q(term=term) & Q(**{f'student__is_active': True})
        if value:
            object_list = self.model.objects.filter(query)
            self.request.session['search'] = self.request.GET.get('q', '')
        else:
            object_list = self.model.objects.filter(Q(term=term) & Q(**{f'student__is_active': True}))
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
            pk=self.kwargs['pk'], is_active=True)
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
                students = Student.objects.filter(clas=dc, is_active=True)

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
    from sms_management.tasks import update_student_debt_view_celery
    update_student_debt_view_celery.delay()
    messages.add_message(request, messages.SUCCESS,
                         f'عملیات بروز رسانی شروع شد لطفا 5 دقیقه صبر کنید و مجددا صفحه را رفرش کنید.')
    return redirect(request.session['last_url'])



def resend_sms_tuition(request, pk, *args, **kwargs):
    """ارسال مجدد پیامک برای شهریه ترم"""
    from sms_management.tasks import send_sms_reminder
    from django.db.models import Sum
    
    try:
        tuition = Tuition.objects.get(id=pk)
        student = tuition.student
        
        # محاسبه مانده حساب متربی
        acc_balance = update_student_debt(student)
        
        # محاسبه مجموع موعدهای پرداخت بعدی
        today = jdatetime.datetime.now().date()
        next_paydays_date = PayDay.objects.filter(
            pay_date__gte=today, 
            is_send_sms=False,
            tuition=tuition
        )
        
        total_next_debts = next_paydays_date.aggregate(total_next_debts=Sum('price'))['total_next_debts']
        if total_next_debts is None:
            total_next_debts = 0
            
        # مقدار بدهی
        debt = acc_balance - total_next_debts
        
        if debt > 0:
            debt_value = "{:,}".format(debt)
            debt_value = f"{debt_value} تومان"
                
            # ارسال پیامک
            if send_sms_reminder(student, debt_value, tuition=tuition):
                messages.add_message(request, messages.SUCCESS, 
                                   f'پیامک برای {student.get_full_name()} با موفقیت ارسال شد.')
            else:
                messages.add_message(request, messages.ERROR, 
                                   f'خطا در ارسال پیامک برای {student.get_full_name()}.')
        else:
            messages.add_message(request, messages.WARNING, 
                               f'متربی {student.get_full_name()} بدهی ندارد.')
            
    except Tuition.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'شهریه مورد نظر یافت نشد.')
    except Exception as e:
        messages.add_message(request, messages.ERROR, f'خطا در ارسال پیامک: {str(e)}')
    
    previous_url = request.META.get('HTTP_REFERER')
    return redirect(previous_url)


def sms_history_modal(request, pk, *args, **kwargs):
    """نمایش تاریخچه پیامک های ارسالی برای شهریه"""
    from sms_management.models import SendedSMS
    from django.utils import timezone
    
    try:
        tuition = Tuition.objects.get(id=pk)
        student = tuition.student
        
        # دریافت پیامک های ارسالی برای این شهریه ترم
        sent_sms = SendedSMS.objects.filter(
            student=student,
            tuition_term=tuition.tuition_term
        ).order_by('-send_date')
        
        # اضافه کردن اطلاعات زمان برای دیباگ
        current_time = timezone.now()
        current_time_local = timezone.localtime(current_time)
        
        context = {
            'student': student,
            'tuition': tuition,
            'sent_sms': sent_sms,
        }
        
        return render(request, 'tuition/sms_history_modal.html', context)
        
    except Tuition.DoesNotExist:
        return render(request, 'tuition/sms_history_modal.html', 
                     {'error': 'شهریه مورد نظر یافت نشد.'})
    except Exception as e:
        return render(request, 'tuition/sms_history_modal.html', 
                     {'error': f'خطا در دریافت اطلاعات: {str(e)}'})


# ==================== Student Financial Status API ====================

class StudentFinancialStatusView(LoginRequiredMixin, View):
    """نمایش صفحه وضعیت مالی برای متربیان"""
    
    def get(self, request, *args, **kwargs):
        # بررسی دسترسی - فقط متربیان
        if not hasattr(request.user, 'student'):
            messages.add_message(request, messages.WARNING, 'فقط متربیان به این صفحه دسترسی دارند')
            return redirect('panel')
        
        context = {
            'page_title': 'وضعیت مالی من',
            'page_description': 'مشاهده بدهی/طلب و پرداخت‌های انجام شده',
            'term': self.request.session['term_title']
        }
        return render(request, 'tuition/student_financial.html', context)


def student_financial_status_api(request):
    """API برای دریافت وضعیت مالی فعلی متربی"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'لطفا وارد حساب کاربری خود شوید'}, status=401)
    
    if not hasattr(request.user, 'student'):
        return JsonResponse({'error': 'دسترسی غیرمجاز'}, status=403)
    
    try:
        student = request.user.student
        
        # بروزرسانی بدهی دانش‌آموز
        account_balance = update_student_debt(student)
        
        # تشخیص بدهی یا طلب
        status_type = 'بدهکار' if account_balance > 0 else ('بستانکار' if account_balance < 0 else 'تسویه شده')
        amount = abs(account_balance)
        amount_formatted = "{:,}".format(amount)
        
        # محاسبه مجموع کل شهریه‌ها
        tuition_all = TuitionTerm.objects.filter(groups=student.clas)
        total_debt = tuition_all.aggregate(total_debt=Sum('price'))['total_debt'] or 0
        
        # محاسبه مجموع کل پرداخت‌ها
        payments = Payment.objects.filter(student=student)
        total_pay = payments.aggregate(total_pay=Sum('amount'))['total_pay'] or 0
        
        # تعداد پرداخت‌ها
        payments_count = payments.count()
        
        data = {
            'status': 'success',
            'account_balance': account_balance,
            'amount': amount,
            'amount_formatted': amount_formatted,
            'status_type': status_type,
            'total_debt': total_debt,
            'total_debt_formatted': "{:,}".format(total_debt),
            'total_pay': total_pay,
            'total_pay_formatted': "{:,}".format(total_pay),
            'payments_count': payments_count,
            'student_name': student.get_full_name(),
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': f'خطا در دریافت اطلاعات: {str(e)}'}, status=500)


def student_payments_list_api(request):
    """API برای دریافت لیست پرداخت‌های متربی با صفحه‌بندی"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'لطفا وارد حساب کاربری خود شوید'}, status=401)
    
    if not hasattr(request.user, 'student'):
        return JsonResponse({'error': 'دسترسی غیرمجاز'}, status=403)
    
    try:
        student = request.user.student
        
        # دریافت شماره صفحه از query parameter
        page_number = request.GET.get('page', 1)
        per_page = request.GET.get('per_page', 10)
        
        # دریافت تمام پرداخت‌های دانش‌آموز
        payments = Payment.objects.filter(student=student).order_by('-pay_date', '-id')
        
        # صفحه‌بندی
        paginator = Paginator(payments, per_page)
        page_obj = paginator.get_page(page_number)
        
        # آماده‌سازی داده‌های پرداخت‌ها
        payments_data = []
        for payment in page_obj:
            payments_data.append({
                'id': payment.id,
                'amount': payment.amount,
                'amount_formatted': payment.amount_view,
                'pay_date': payment.jd_pay_date,
                'pay_type': payment.get_pay_type_display(),
                'term': str(payment.term),
                'description': payment.desc or 'ندارد'
            })
        
        data = {
            'status': 'success',
            'payments': payments_data,
            'pagination': {
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
                'total_count': paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
                'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
                'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
            }
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': f'خطا در دریافت اطلاعات: {str(e)}'}, status=500)