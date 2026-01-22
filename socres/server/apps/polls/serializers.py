from rest_framework import serializers
from .models import *
from ..jwt_auth.models import BaseUser


class PollSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Poll
        fields = ['theme', 'description', 'user']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionModel
        fields = ['poll', 'question', 'field_type']

class BaseFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseField
        fields = ['question', 'note']

class RadioChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadioChoice
        fields = ['question', 'text']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['poll', 'user', 'field', 'answer']



