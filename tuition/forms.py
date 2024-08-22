from django import forms
from kanon_moslem.aminBaseViews import *
from kanon_moslem.datetimeUtils import change_date_to_english
from tuition.models import Payment


class PaymentCreateForm(BaseFormKanon):
    pay_date = forms.CharField(label='تاریخ پرداخت',
                              widget=forms.TextInput(attrs={'placeholder': 'تاریخ را انتخاب کنید'}))

    def __init__(self, *args, **kwargs):
        super(PaymentCreateForm, self).__init__(*args, **kwargs)
        self.fields['student'].disabled = True
        self.fields['term'].disabled = True

    class Meta:
        model = Payment
        fields = [
            "student",
            "term",
            "amount",
            "pay_date",
            "pay_type",
        ]

    def clean_pay_date(self):
        pay_date = self.cleaned_data['pay_date']
        try:
            pay_date = change_date_to_english(pay_date, 2)
        except:
            pay_date = None
        return pay_date
