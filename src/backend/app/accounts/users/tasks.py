
from celery import shared_task

from utils.otp import OtpManager, OtpMassageTemplate


@shared_task
def send_otp_code(phone_number, code, template):
    """
    send_otp_code 
    send otp code in view register otp and login otp 

    _extended_summary_

    Args:
        phone_number (str): 0901204325
        code (str): 5010   
        template (str): schema example => register | login
    Returns:
        bool
    """
    otp = OtpManager()
    otp.send_sms(phone_number=phone_number, code=code, template=template)
    return True
    


