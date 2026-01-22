from django.shortcuts import render
from django.contrib.auth.models import User
from django.http.response import *
from django.utils.datastructures import MultiValueDictKeyError
from django.views import generic as views
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from rest_framework_simplejwt.serializers import TokenRefreshSerializer


from .serializers import *
from .forms import *
from json import JSONEncoder

from datetime import timedelta
from random import randint


# Create your views here.

class UserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CookieTokenObtainPairView(TokenObtainPairView):
    
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)
        response.set_cookie(
            key='access_token',
            value=response.data['access'],
            expires=timedelta(minutes=5),
        )
        response.set_cookie(
            key='refresh_token',
            value=response.data['refresh'],
            expires=timedelta(days=1),
        )
        return response
    
class CookieTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs) -> Response:
        try:
            request.COOKIES['refresh_token']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = super().get_serializer(data={'refresh': request.COOKIES['refresh_token']})
        try:
            serializer.is_valid()
        except TokenError:
            response = Response(status=status.HTTP_403_FORBIDDEN)
            response.delete_cookie('refresh_token')
            response.delete_cookie('access_token')
            return response
        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=serializer.data['access'],
            expires=timedelta(minutes=5),
        )
        response.set_cookie(
            key='refresh_token',
            value=serializer.data['refresh'],
            expires=timedelta(days=1),
        )
        return response
            
class RegisterView(views.FormView):
    form_class = RegisterForm
    template_name = 'components\\register-form.html'
    
    def get(self, request: Request, *args, **kwargs):
        return render(request=request, template_name=self.template_name, context={'form': self.form_class})
    def post(self, request: Request, *args, **kwargs) -> User:
        form = self.get_form()
        if (form.is_valid()):
            user_serializer = UserSerializer(data={
                'username': f'user_{str(randint(1, 1000000000000000000))}',
                'password': form.data['password'],
            })

            if user_serializer.is_valid():
                base_user_serializer = BaseUserSerializer(data={
                    'user': user_serializer.save().id,
                    'phone_number': form.data['phone'],
                })

                if (base_user_serializer.is_valid()):
                    base_user = base_user_serializer.save()
                    return JsonResponse({'username': base_user.user.username, 'password': form.data['password']})
        print(base_user_serializer.errors, user_serializer.errors)
        
        return HttpResponseBadRequest()
    
class LoginView(views.FormView):
    form_class = LoginForm
    template_name = 'components\\login-form.html'
    
    def get(self, request: Request, *args, **kwargs):
        return render(request=request, template_name=self.template_name, context={'form': self.form_class})
    
    def post(self, request: Request, *args, **kwargs) -> User:
        form = self.get_form()
        if (form.is_valid()):
            try:
                user = User.objects.get(id=BaseUser.objects.get(phone_number=form.data['phone']).id)
                if (user.check_password(form.data['password'])):
                    return JsonResponse({'username': user.username, 'password': form.data['password']})
                else:
                    return HttpResponseForbidden()
            except ObjectDoesNotExist:
                return HttpResponseForbidden()

