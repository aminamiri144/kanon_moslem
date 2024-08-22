from django.urls import path
from .views import *

urlpatterns = [
    path('list/', TuitionMainView.as_view(), name='tuition-list'),
    path('payments/<int:pk>', PaymentsOfStudentListView.as_view(), name='payments-list'),
    path('payments/add/<int:pk>', CreatePaymentView.as_view(), name='add-payment'),
]