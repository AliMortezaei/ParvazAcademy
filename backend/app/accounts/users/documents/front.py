
from drf_spectacular.utils import OpenApiResponse,extend_schema_serializer, OpenApiExample, extend_schema




def login_email():
    login_email = extend_schema(
        examples=[OpenApiExample('UserLoginEmail', 
            value={
                'email': 'alireza2324@gmail.com',
                'password': 'aliwww29432',
            },)
        ],
        responses={
            201:OpenApiResponse(
                response={'token': {'access': 'asfasf.asfsaf.asfsaf', 'refresh': 'asfasfsaf'}, 'user_type': 'student'},
                examples=[OpenApiExample('responsess', 
                    value={'token': {'access': 'asfasf.asfsaf.asfsaf', 'refresh': 'asfasfsaf'}, 'user_type': 'student'},)
                ],
                description= "Response token `access`, `refresh` and `user_type` ",
            )
        } 
        
    )
    return login_email



def verify_doc():
    verify = extend_schema(
        examples=[OpenApiExample('UserVerify', 
            value={
                'phone_number': '09163261462',
                'code': '29432',
            },)
        ],
        responses={
            201:OpenApiResponse(
                response={'token': {'access': 'asfasf.asfsaf.asfsaf', 'refresh': 'asfasfsaf'}, 'user_type': 'student'},
                examples=[OpenApiExample('responsess', 
                    value={'token': {'access': 'asfasf.asfsaf.asfsaf', 'refresh': 'asfasfsaf'}, 'user_type': 'student'},)
                ],
                description= "Response token `access`, `refresh` and `user_type` ",
            )
        } 
        
    )
    return verify
    
def register_doc():
    register = extend_schema(
        examples=[OpenApiExample('UserRegister_1', 
            value={
                'email': 'parvaz@example.com',
                'full_name': 'alirez mortezaei',
                'phone_number': '09163261462',
                'password': 'parvaz_2324',
            },)
        ],
        responses={
            202:OpenApiResponse(
                response= {'phone_number': '09182643715'},
                examples= [OpenApiExample('responses', value={'phone_number': '09182643715'})],
                description= "a phone_number to send otp code ",
            )
        } 
        
    )
    return  register


def login_otp_doc():
    login_otp = extend_schema(
        examples=[OpenApiExample('UserLoginOtp_1', 
            value={
                'phone_number': '09163261462',
            },)
        ],
        responses={
            202:OpenApiResponse(
                response= {'phone_number': '09182643715'},
                examples= [OpenApiExample('responses', value={'phone_number': '09182643715'})],
                description= "a phone_number to send otp code ",
            )
        } 
        
    )

    return login_otp