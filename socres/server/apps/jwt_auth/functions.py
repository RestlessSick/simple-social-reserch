from rest_framework.request import Request
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import BaseUser

def get_user(request: Request) -> BaseUser:
    try:
        token = AccessToken(token=request.COOKIES.get('access_token'), verify=True)

        return BaseUser.objects.get(id=token.payload['user_id'])

    except KeyError:
        raise TokenError('Отсутствует access_token')
    