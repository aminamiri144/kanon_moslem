import os
from celery import shared_task
from datetime import datetime, timedelta
from logger.views import log
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
import jdatetime
from members.models import Student
from sms_management.sms import SMS
from sms_management.models import SendedSMS
from tuition.views import update_student_debt
from tuition.models import PayDay


def send_sms_reminder(student, debt_value, payday):
    bodyID = int(os.getenv("BODY_ID_PAYDAY_REMINDER", '245523'))
    fullname = student.get_full_name()
    args = [fullname, debt_value]

    if student.father_phone is not None:
        phone_number = student.father_phone
    elif student.mather_phone is not None:
        phone_number = student.mather_phone
    else:
        phone_number = student.mobile

    try:
        sms = SMS()
        sms_response = sms.send_service_sms(body_id=bodyID, phone_number=phone_number, args=args)
        if sms_response.status_code == 200:
            res = sms_response.json()
            ss = SendedSMS()
            ss.student = student
            ss.last_status = res['status']
            ss.to_number = phone_number
            try:
                ss.recId = res['recId']
            except Exception as e:
                log('SYSTEM', f'{e}', 'send_sms_reminder')
            ss.pattern_id = bodyID
            ss.title = f'اطلاع رسانی وعده پرداخت {fullname} مقدار {debt_value}'
            ss.save()

            payday.is_send_sms = True
            payday.sms = ss
            payday.save()
            return True
    except Exception as e:
        log('SYSTEM', f'{e}', 'send_sms_reminder')
    return False


@shared_task()
def payday_reminder_sms():
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    tomorrow_paydays = PayDay.objects.filter(pay_date=tomorrow, is_send_sms=False)
    for payday in tomorrow_paydays:
        # مانده حساب متربی
        acc_balance = update_student_debt(payday.tuition.student)
        # تاریخ پس فردا
        day_after_tomorrow = today + timedelta(days=2)
        # موعد های پرداخت بعدی
        next_paydays_date = PayDay.objects.filter(pay_date__gte=day_after_tomorrow, is_send_sms=False,
                                                  tuition=payday.tuition)
        # مجموع مبلغ قسط های بعدی (غیر فردا)

        total_next_debts = next_paydays_date.aggregate(total_next_debts=Sum('price'))['total_next_debts']
        if total_next_debts is None:
            total_next_debts = 0
        # مقدار بدهی
        debt_value = "{:,}".format(acc_balance - total_next_debts)
        try:
            send_sms_reminder(payday.tuition.student, debt_value, payday)
        except Exception as e:
            log('CELERY_BEAT', f'{e}', 'payday_reminder_sms')


@shared_task()
def update_student_debt_view_celery():
    students = Student.objects.all()
    for student in students:
        update_student_debt(student)
