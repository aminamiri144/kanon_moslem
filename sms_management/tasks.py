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


def send_sms_reminder(student, debt_value, payday=None, tuition=None):
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
            ss.to_number = phone_number
            ss.pattern_id = bodyID
            ss.title = f'مبلغ بدهی {debt_value}'
            
            # تعیین وضعیت بر اساس پاسخ API
            if 'recId' in res and res['recId']:
                try:
                    rec_id = str(res['recId'])
                    # اگر recId یک عدد بیش از 15 رقم باشد، ارسال موفق است
                    if rec_id.isdigit() and len(rec_id) > 15:
                        ss.last_status = 'success'
                        ss.recId = rec_id
                    else:
                        # در غیر این صورت، recId همان کد خطا است
                        ss.last_status = rec_id
                        ss.recId = rec_id
                except Exception as e:
                    log('SYSTEM', f'{e}', 'recId processing error')
                    ss.last_status = '0'  # خطای نامشخص
                    ss.recId = '-1'
            else:
                # اگر recId وجود نداشته باشد، از status استفاده کن
                ss.last_status = str(res.get('status', '0'))
                ss.recId = '-1'
            
            # اضافه کردن اطلاعات شهریه ترم
            if hasattr(payday, 'tuition') and payday.tuition:
                ss.tuition_term = payday.tuition.tuition_term
                ss.term = payday.tuition.term

            if tuition:
                ss.tuition_term = tuition.tuition_term
                ss.term = tuition.term 

            ss.save()
            
            # فقط در صورت ارسال موفق، وضعیت payday را تغییر بده
            if payday:
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
    tomorrow_paydays = PayDay.objects.filter(pay_date=tomorrow, is_send_sms=False, is_paid=False)
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
        debt = acc_balance - total_next_debts
        if debt > 0:
            debt_value = "{:,}تومان".format(debt)
            try:
                send_sms_reminder(payday.tuition.student, debt_value, payday)
            except Exception as e:
                log('CELERY_BEAT', f'{e}', 'payday_reminder_sms')


@shared_task()
def update_student_debt_view_celery():
    students = Student.objects.all()
    for student in students:
        update_student_debt(student)
