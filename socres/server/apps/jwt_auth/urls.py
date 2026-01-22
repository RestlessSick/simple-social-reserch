from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

from .views import *
app_name = 'socres.server.apps.jwt_auth'

router = DefaultRouter()
router.register(r'list', UserViewSet)


urlpatterns = [
    path('users/', include(router.urls), name='users'),
    path('', include('rest_framework.urls'), name='base-auth'),
    path('token/obtain/', CookieTokenObtainPairView.as_view(), name='obtain-token'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='refresh-token'),

    path('register/', RegisterView.as_view(), name='register'),
    path('Login/', LoginView.as_view(), name='login'),
]
