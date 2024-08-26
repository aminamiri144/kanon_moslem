from django.urls import path
from .views import *

urlpatterns = [
    path('list/', TuitionMainView.as_view(), name='tuition-list'),
    path('payments/<int:pk>', PaymentsOfStudentListView.as_view(), name='payments-list'),
    path('payments/add/<int:pk>', CreatePaymentView.as_view(), name='add-payment'),
    path('payday/create/<int:pk>', PayDateCreate.as_view(), name='paydate-create'),
    path('payday/list/<int:pk>', PayDayOfTuitionListView.as_view(), name='payday-list'),
    path('payday/payed/<int:pk>', pay_day_payed_make_true, name='payday-payed'),
    path('generate/', TuitionTermGenerate.as_view(), name='generate-term-tuitions'),
]