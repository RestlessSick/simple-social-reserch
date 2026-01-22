from django import template
from ..models import *
from django import forms

register = template.Library()


@register.simple_tag
def get_fields(question: QuestionModel):
    return BaseField.objects.filter(question=question)

@register.simple_tag
def get_radio_choices(question: QuestionModel):
    return RadioChoice.objects.filter(question=question).order_by('position')

@register.simple_tag
def get_poll_questions(poll: Poll):
    return QuestionModel.objects.filter(poll=poll)

