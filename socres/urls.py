from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api-auth/', include('socres.server.apps.jwt_auth.urls', namespace='auth')),
    path('', include('socres.server.apps.main.urls', namespace='main')),
    path('polls', include('socres.server.apps.polls.urls', namespace='polls')),
]
