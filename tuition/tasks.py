import os

import jdatetime
from celery import shared_task

from sms_management.sms import SMS
from tuition.models import Tuition


@shared_task()
def send_sms_of_debts():
    tuitions = Tuition.objects.filter(is_paid=False)
    # دریافت تاریخ امروز به شمسی
    today_shamsi = jdatetime.date.today()
    # دریافت نام ماه شمسی
    month_name_shamsi = today_shamsi.strftime("%B")
    for tuition in tuitions:
        a = tuition.tuition_term.price / 3
        formatted_value = int(a) if a.is_integer() else a
        amount = "{:,}".format(formatted_value)
        name = tuition.student.get_full_name()
        args = [month_name_shamsi, name, amount]

        if tuition.student.father_phone is not None:
            phone_number = tuition.student.father_phone
        else:
            phone_number = tuition.student.mobile
        body_id = int(os.getenv("SMS_BODY_ID_DEBT", '243281'))
        sms = SMS()
        result = sms.send_service_sms(
            body_id=body_id,
            args=args,
            phone_number=phone_number,
        )
        res = result.json()
        from sms_management.models import SendedSMS
        SendedSMS(
            title='موعد شهریه',
            to_number=phone_number,
            send_type='shared',
            pattern_id=body_id,
            student=tuition.student,
            last_status=res['status']
        ).save()


@shared_task()
def check_and_send_sms_of_debts():
    today_shamsi = jdatetime.date.today()
    # بررسی اینکه آیا امروز اول ماه شمسی است
    if today_shamsi.day == int(os.getenv("DAT_OF_MONTH_TO_SEND_DEBT_SMS", '1')):
        send_sms_of_debts.delay()
