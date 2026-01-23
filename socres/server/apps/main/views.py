from django.shortcuts import render
from django.views import generic
from ....settings import STATIC_ROOT
import os


# Create your views here.

from ..jwt_auth.functions import *
from ..polls.models import *
class IndexView(generic.TemplateView):
    template_name='main/index.html'



class ProfileView(generic.TemplateView):
    template_name = 'main/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = get_user(self.request)
        context["answers"] = Answer.objects.filter(user=get_user(self.request)).order_by('poll', 'field')
        return context
    
class AboutView(generic.TemplateView):
    template_name = 'main/about.html'
    


