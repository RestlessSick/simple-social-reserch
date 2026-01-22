from django.urls import include, path
from .views import *

app_name = 'socres.server.apps.polls'

urlpatterns = [
    path('/create/', Polls.as_view({'get': 'list', 'post': 'create'}), name='poll'),
    path('/form-gen/question-<int:id>/', QuestionForm.as_view(), name='question-form'),
    path('/form-gen/question-<int:qid>-<slug:field_type>-<int:id>/', FieldForm.as_view(), name='field-form'),
    path('/<int:id>/', PollView.as_view({'get': 'get', 'post': 'post'}), name='single-poll'),
    path('/gen-qr/<int:id>/', gen_qr, name='qr'),
    path('/gen-url/<int:id>/', gen_url, name='url'),
    path('/', PollsPagination.as_view(), name='polls')
]
