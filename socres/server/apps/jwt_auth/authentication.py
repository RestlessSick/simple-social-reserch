from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, ExpiredTokenError

from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy


class JWTCookieAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            token = AccessToken(request.COOKIES.get('access_token'), verify=True)
            token.verify()


            return User.objects.get(id=token.payload['user_id']), token.token
        except TokenError as error:
            print(error)
            return None
        except KeyError as error:
            print(error)
            return None
        
