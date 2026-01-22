from django.shortcuts import render
from django.views import generic as views
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import status
from rest_framework_simplejwt.tokens import *
from wsgiref.util import FileWrapper
import qrcode
import random


from .models import *
from .serializers import *
from ..jwt_auth.functions import get_user


# Create your views here.

class PollsPagination(views.ListView):
    queryset = Poll.objects.all().order_by('-date_created')
    template_name = 'components\\poll-cards.html'
    paginate_by = 4


class PollView(ViewSet): #Ну вот не может он найти csrfmiddlewaretoken, ну вот никак вообще
    poll_model = Poll
    permission_classes = [IsAuthenticated]
    def get(self, request, id, *args, **kwargs):
        return render(request=request, template_name='polls\\poll.html', context={'poll': self.poll_model.objects.get(id=id), 'questions': QuestionModel.objects.filter(poll=self.poll_model.objects.get(id=id))})
    
    def post(self, request: Request, id, *args, **kwargs):

        to_save = list()

        for key in request.data:

            try: 
                token = AccessToken(token=request.COOKIES.get('access_token'), verify=True)
                try:
                    Answer.objects.get(poll=id, field=key.split('-')[2], user=BaseUser.objects.get(user=User.objects.get(id=token.payload['user_id'])).id)
                    raise Exception
                except ObjectDoesNotExist:
                    pass
            except:
                return Response(status=status.HTTP_403_FORBIDDEN)

            serializer = AnswerSerializer(data={
                'poll': id,
                'field': key.split('-')[2],
                'user': BaseUser.objects.get(user=User.objects.get(id=token.payload['user_id'])).id,
                'answer': request.data[key],
            })

            if serializer.is_valid():
                to_save.append(serializer)
            else:
                print(serializer.error_messages, serializer.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        
        for el in to_save:
            el.save()

        return Response(status=status.HTTP_201_CREATED)

class Polls(ViewSet):

    queryset = Poll.objects.all()


    def list(self, request):
        return render(request=request, template_name='polls\\create-poll.html', context={})
    
    def create(self, request: Request):
        data = request.data['Poll']
        print(data)
        poll = PollSerializer(data={
            'theme': data['theme'],
            'description': data['description'],
            'user': get_user(request=request).id,
            })
        
        
        if (poll.is_valid()):
            poll = poll.create(poll.validated_data)
        else:
            print(poll.error_messages, poll.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
        
        for q in data['questions']:
            question = QuestionSerializer(data={
                'poll': poll.id,
                'question': q['question'],
                'field_type': q['field_type']
            })
            if (question.is_valid()):
                question = question.create(question.validated_data)
            else:
                print(question.error_messages, question.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            if (question.field_type == 'RadioField'):
                for c in q['choices']:
                    choice = RadioChoiceSerializer(data={
                        'question': question.id,
                        'text': c['text'],
                    })

                    if (choice.is_valid()):
                        choice.create(choice.validated_data)
                    else: 
                        print(choice.error_messages, choice.errors)
                        Response(status=status.HTTP_400_BAD_REQUEST)

            for f in q['fields']:
                field = BaseFieldSerializer(data={
                    'question': question.id,
                    'note': f['note'],
                })

                if (field.is_valid()):
                    field.create(field.validated_data)
                else: 
                    print(field.error_messages, field.errors)
                    Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)

def gen_qr(request, id, *args, **kwargs):
    qr = qrcode.make(f'{request.META['HTTP_REFERER']}{reverse_lazy('polls:single-poll', kwargs={'id': id})}')
    name = f'{str(random.random())[2::]}.png'
    qr.save(f'tmp\\{name}')
    
    file = open(f'tmp\\{name}', 'rb')
    return HttpResponse(FileWrapper(file), content_type='application/png')

def gen_url(request, id, *args, **jwargs):
    return HttpResponse(f'{request.META['HTTP_HOST']}{reverse_lazy('polls:single-poll', kwargs={'id': id})}')
    
class QuestionForm(APIView):
    
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    
    template_name = 'components\\question-form.html'

    def get(self, request, id, *args, **kwargs):
        return render(request=request, template_name=self.template_name, context={'id': id})
    
    
    
class FieldForm(QuestionForm): 
    template_name = 'components\\field-form.html'

    def get(self, request, qid, field_type, id, *args, **kwargs): # Ужас какой 
        if field_type == 'ChoiceField':
            return render(request=request, template_name='components\\choice-field.html', context={'qid': qid, 'id': id, 'field_type': field_type})
        else:
            return render(request=request, template_name=self.template_name, context={'qid': qid, 'id': id, 'field_type': field_type})