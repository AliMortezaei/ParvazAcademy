
from celery import shared_task

from utils.otp import OtpManager, OtpMassageTemplate


@shared_task
def send_otp_code(phone_number, code):
    template = OtpMassageTemplate() 
    otp = OtpManager()
    message = template.regster(message=code)
    otp.send_sms(receptor=phone_number, message=message)
    return True
    


