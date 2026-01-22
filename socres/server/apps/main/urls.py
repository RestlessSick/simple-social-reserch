from django.urls import path
from .views import *
app_name = 'socres.server.apps.main'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('about/', AboutView.as_view(), name='about'),
]