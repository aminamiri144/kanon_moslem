from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View, ListView, CreateView

from kanon_moslem.aminBaseViews import AminView, BaseCreateViewAmin
from kanon_moslem.views import NoStudent, LoginRequiredMixin, SuccessMessageMixin
from .forms import PaymentCreateForm
from .models import *
from django.db.models import Q


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
        return reverse('tuition-list')
