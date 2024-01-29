from rest_framework.exceptions import APIException
from rest_framework import status


class ServiceUnavailableException(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailabl'


class VerifyUserException(APIException):
    status_code = 403
    default_detail = 'شما مجاز به انجام این کار نیستید.'


class NotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'محتوا یافت نشد'

class InvaliedCodeVrify(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'کد وارد شده اشتباه است'

class UserNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'کاربر یافت نشد'