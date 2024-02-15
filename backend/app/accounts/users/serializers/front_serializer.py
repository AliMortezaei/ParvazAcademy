from django.utils.translation import gettext_lazy as _


from rest_framework import serializers, validators
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

from ..models import User




def validate_type_code(value):
    if not value.isdigit():
        raise serializers.ValidationError('کد باید شامل اعداد باشد.')
    if len(value) != 5:
        raise serializers.ValidationError('کد باید ۵ رقمی باشد.')
    return value

def validate_phone_number(phone_number):

    if (not phone_number.isdigit()) \
        or (len(phone_number) != 11) \
        or (phone_number[:2] != "09"):
        raise serializers.ValidationError('شماره تماس صحیح نیست')
    return phone_number


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["full_name" ,"email", "phone_number", "password"]





@extend_schema_serializer(
    examples=[
        OpenApiExample('UserVerify_1', 
        summary='Create_user after verify' ,
        value={
            'phone_number': '09163261462',
            'code': '58964',
        })
    ]
)
class UserVerifySerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=5, validators=[validate_type_code])
    phone_number = serializers.CharField(
        required=True,
        max_length=11,
        validators=[validate_phone_number]
    )        
    class Meta:
        model = User
        fields = ["phone_number", "code"]
        #validators = []  # Remove a default "unique together" constraint.




@extend_schema_serializer(
    examples=[
        OpenApiExample('UserLogin_1', 
        summary='User Login by phone number' ,
        value={
            'phone_number': '09163261462',
        })
    ]
)
class UserLoginOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        required=True,
        max_length=11,
        validators=[validate_phone_number]
    ) 

    def login_validate(self, attrs):
        phone_number = attrs.get('phone_number')

        if phone_number:
            user = User.objects.filter(phone_number=phone_number).first()
            if user is None:
                msg = _('phone number not found')
                raise serializers.ValidationError(msg, code='not found')
        else:
            msg = _('Must include phone number')
            raise serializers.ValidationError(msg)            

        attrs.update({
            'phone_number': user.phone_number,
            'full_name': user.full_name,
            'email': user.email,
            'password': '',
        })
        
        return attrs


@extend_schema_serializer(
    examples=[
        OpenApiExample('UserLogin_1', 
        summary='User Login by email and password' ,
        value={
            'email': 'parvaz@example.com',
            'password': '2424143'
        })
    ]
)
class UserLoginEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ["email", "password"]
        

    