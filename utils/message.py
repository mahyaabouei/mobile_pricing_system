import requests
import os




class MessageMelipayamak():
    def __init__(self):
        self.username = "9011010959"
        self.password = "@8F20"
        self.url ="https://rest.payamak-panel.com/api/SendSMS/BaseServiceNumber"
        self.bodyId = 130566
    def otpSMS(self,otp,mobile):
        data = {
            "username":self.username,
            "password":self.password,
            "text":str(otp),
            "to":str(mobile),
            "bodyId":self.bodyId
        }
        headers = {
            "Content-Type":"application/json"
        }
        resp = requests.post(url=self.url,json=data,headers=headers).text
        return resp

