from django import forms

from education_management.models import Term
from kanon_moslem.aminBaseViews import *
from kanon_moslem.datetimeUtils import change_date_to_english
from .models import Tuition, PayDay, Payment


class PaymentCreateForm(BaseFormKanon):
    pay_date = forms.CharField(label='تاریخ پرداخت',
                               widget=forms.TextInput(attrs={'placeholder': 'تاریخ را انتخاب کنید'}))
    amount = forms.CharField(label='مبلغ پرداخت', widget=forms.TextInput(attrs={'placeholder': 'مبلغ پرداخت را'}))

    def __init__(self, *args, **kwargs):
        super(PaymentCreateForm, self).__init__(*args, **kwargs)
        self.fields['student'].disabled = True
        self.fields['term'].disabled = True
        # اگر در حال ویرایش هستیم
        if self.instance and self.instance.pk:
            # اگر amount منفی است، is_debt را True می‌کنیم و amount را مثبت نمایش می‌دهیم
            if self.instance.amount < 0:
                self.initial['is_debt'] = True
                self.initial['amount'] = abs(self.instance.amount)
            else:
                self.initial['is_debt'] = False
                self.initial['amount'] = self.instance.amount
            # تنظیم pay_date برای نمایش
            if self.instance.pay_date:
                self.initial['pay_date'] = str(self.instance.pay_date).replace('-', '/')

    class Meta:
        model = Payment
        fields = [
            "student",
            "term",
            "amount",
            "pay_date",
            "pay_type",
            "desc",
            "is_debt",
        ]

    def clean_pay_date(self):
        pay_date = self.cleaned_data['pay_date']
        try:
            pay_date = change_date_to_english(pay_date, 2)
        except:
            pay_date = None
        return pay_date

    def clean_amount(self):
        amount = self.cleaned_data['amount'].replace(',', '')
        return int(amount)


class TuitionForm(forms.Form):
    title = forms.CharField(max_length=255, label='عنوان')
    tuition_amount = forms.CharField(label='مبلغ شهریه',
                                     widget=forms.TextInput(attrs={'placeholder': 'مبلغ شهریه ترم به تومان'}))
    term = forms.ModelChoiceField(queryset=Term.objects.all(), label='ترم')
    dore = forms.IntegerField(label='دوره')
    desc = forms.CharField(max_length=255, label='توضیحات')

    def __init__(self, *args, **kwargs):
        super(TuitionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_tuition_amount(self):
        tuition_amount = self.cleaned_data['tuition_amount'].replace(',', '')
        return int(tuition_amount)


class PayDateCreateForm(forms.ModelForm):
    pay_date = forms.CharField(label='موعد پرداخت ',
                               widget=forms.TextInput(attrs={'placeholder': 'تاریخ را انتخاب کنید'}))
    price = forms.CharField(label='مبلغ پرداخت', widget=forms.TextInput(attrs={'placeholder': 'مبلغ پرداخت را'}))

    class Meta:
        model = PayDay
        fields = [
            'tuition',
            'pay_date',
            'price',
        ]

    def __init__(self, *args, **kwargs):
        super(PayDateCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['tuition'].disabled = True

    def clean_pay_date(self):
        pay_date = self.cleaned_data['pay_date']
        try:
            pay_date = change_date_to_english(pay_date, 2)
        except:
            pay_date = None
        return pay_date

    def clean_price(self):
        price = self.cleaned_data['price'].replace(',', '')
        return int(price)
