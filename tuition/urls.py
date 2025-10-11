from django.urls import path
from .views import *
from sms_management.tasks import payday_reminder_sms

urlpatterns = [
    path('list/', TuitionMainView.as_view(), name='tuition-list'),
    path('payments/<int:pk>', PaymentsOfStudentListView.as_view(), name='payments-list'),
    path('payments/add/<int:pk>', CreatePaymentView.as_view(), name='add-payment'),
    path('payday/create/<int:pk>', PayDateCreate.as_view(), name='paydate-create'),
    path('payday/list/<int:pk>', PayDayOfTuitionListView.as_view(), name='payday-list'),
    path('payday/payed/<int:pk>', pay_day_payed_make_true, name='payday-payed'),
    # path('payday/resend-sms/<int:pk>', resend_sms_payday, name='resend-sms-payday'),
    path('resend-sms/<int:pk>', resend_sms_tuition, name='resend-sms-tuition'),
    path('sms-history/<int:pk>', sms_history_modal, name='sms-history-tuition'),
    path('generate/', TuitionTermGenerate.as_view(), name='generate-term-tuitions'),
    path('usd/', update_students_debt_view, name='update-students-debts'),
    
    # Student Financial Status - فقط برای متربیان
    path('my-financial/', StudentFinancialStatusView.as_view(), name='student-financial'),
    path('api/my-status/', student_financial_status_api, name='student-financial-status-api'),
    path('api/my-payments/', student_payments_list_api, name='student-payments-list-api'),
]