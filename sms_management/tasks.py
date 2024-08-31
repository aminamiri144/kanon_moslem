import os

import jdatetime
from celery import shared_task
from datetime import datetime, timedelta

from kanon_moslem.datetimeUtils import gregorian_to_jalali
from sms_management.sms import SMS
from sms_management.models import SendedSMS

from tuition.models import PayDay


def send_sms_reminder(student, month, payday):
    bodyID = int(os.getenv("BODY_ID_PAYDAY_REMINDER", '243281'))
    fullname = student.get_full_name()
    args = [month, fullname, payday.price_view]

    if student.father_phone is not None:
        phone_number = student.father_phone
    elif student.mother_phone is not None:
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
            ss.recId = res['recId']
            ss.pattern_id = bodyID
            ss.title = f'اطلاع رسانی وعده پرداخت {fullname} ماه {month}'
            ss.save()

            payday.is_send_sms = True
            payday.sms = ss
            payday.save()
            return True
    except Exception as e:
        print(f"Error In send_sms_reminder: {e}")
    return False


@shared_task()
def payday_reminder_sms():
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    jalali_date = gregorian_to_jalali(int(tomorrow.year), int(tomorrow.month), int(tomorrow.day))
    tomorrow_paydays = PayDay.objects.filter(pay_date=tomorrow, is_send_sms=False)
    jd_date = jdatetime.date(jalali_date[0], jalali_date[1], jalali_date[2])
    for payday in tomorrow_paydays:
        send_sms_reminder(payday.tuition.student, jd_date.strftime('%B'), payday)
