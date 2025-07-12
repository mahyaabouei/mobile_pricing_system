from django.conf import settings
import requests
import os


class Message():
    def __init__(self,otp,mobile):
        self.otp = otp
        self.mobile = mobile
    def otpSMS(self):
        txt = f'به ایساتیس کراد خوش آمدید \n کد تایید :{self.otp}\nisatiscrowd.ir'
        resp = requests.get(url=f'http://tsms.ir/url/tsmshttp.php?from={os.getenv("SMS_NUMBER")}&to={self.mobile}&username={os.getenv("SMS_USERNAME")}&password={os.getenv("SMS_PASSWORD")}&message={txt}').json()
        return resp