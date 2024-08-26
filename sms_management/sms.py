import os
import requests



class SMS:
    def __init__(self):
        self.token = os.getenv('SMS_TOKEN', 'a5763c34c5414be0811be12635620a44')

    def send_service_sms(self, body_id: int, phone_number: str, args: list):
        url = f"https://console.melipayamak.com/api/send/shared/{self.token}"
        data = {'bodyId': body_id, 'to': phone_number, 'args': args}
        response = requests.post(url=url, json=data)
        """
            {
                "recId": 3741437414,
                "status": "شرح خطا در صورت بروز"
            }
        """
        return response


    def get_send_status(self, recIds: list):
        url = f"https://console.melipayamak.com/api/receive/status/{self.token}"
        data = {'recIds': recIds}
        response = requests.post(url=url, json=data)
        """
            {
                "results": ['ارسال شده' ,'ارسال نشده'],
                "resultsAsCode": [-1, 200],
                "status": "شرح خطا در صورت بروز"
            }
        """
        return response