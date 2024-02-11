from typing import Callable
import random
from kavenegar import *

from .exception import ServiceUnavailableException
from core import settings

class OtpMassageTemplate:

    def regster(self, message: str) -> str:
        return f'{message} کد تایید شما '

    def login(self, message: str) -> str:
        return f'{message} کد ورود شما'
    

class OtpManager:

    def __init__(self):
        self.otp = KavenegarAPI(settings.OTP_KAVENEGAR_KEY)

    def send_sms(self, receptor: str, message: Callable[..., str]):
        try:
           
            response = self.otp.sms_send(
                params = {
                    'sender': '',
                    'receptor': receptor,
                    'message': message,
                }
            )
        except (APIException, HTTPException) as exp:
            raise ServiceUnavailableException()
            
    @staticmethod    
    def generate_otp_code() -> int:
        random_code = random.randint(10000, 99999)
        return random_code