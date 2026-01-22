from django.db import models
from ...apps.jwt_auth.models import *

from datetime import datetime

# Create your models here.


field_types = (
    ('RadioField', 'Radio Field'),
    ('TextField', 'Text Field'),
    ('TextArea', 'Text Area'),
    ('NumberField', 'Number Field'),
    # 'date_field',
)



class Poll(models.Model):
    theme = models.TextField(max_length=30)
    description = models.TextField(max_length=1000)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_created=True, editable=False, default=datetime.now())

    def __str__(self):
        return f'Poll object {self.id} with {QuestionModel.objects.filter(poll=Poll.objects.get(id=self.id)).__len__()} questions'


class QuestionModel(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)

    field_type = models.TextField(choices=field_types)
    position = models.IntegerField(auto_created=True, editable=False)

    def __str__(self):
        return f'Question of: {self.poll}; with text: {self.question};'
    
    def save(self, *args, **kwargs):
        try:
            self.position = list(QuestionModel.objects.filter(poll=self.poll).values_list('position'))[-1][0] + 1
        except IndexError:
            self.position = 1
        # if tuple([self.position, ]) in QuestionModel.objects.filter(poll=self.poll).values_list('position'):
        #     raise ValueError('There already is object with this position number.')

        return super().save(*args, **kwargs)
    
    


class RadioChoice(models.Model):
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)
    text = models.TextField(max_length=30)
    position = models.IntegerField()

    def save(self, *args, **kwargs):
        try:
            self.position = list(RadioChoice.objects.filter(question=self.question).values_list('position'))[-1][0] + 1
        except IndexError:
            self.position = 1
        # if tuple([self.position, ]) in QuestionModel.objects.filter(poll=self.poll).values_list('position'):
        #     raise ValueError('There already is object with this position number.')

        return super().save(*args, **kwargs)

class BaseField(models.Model):
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)
    note = models.TextField(max_length=16)


class Answer(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    field = models.ForeignKey(BaseField, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1000)

