from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from phonenumber_field.serializerfields import *

from .models import *

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        password = self.validated_data.pop('password')
        user = super().create()
        user.set_password(password)

        return user
    
    def save(self):
        password = self.validated_data.pop('password')
        user = User.objects.create(username=self.validated_data['username'])
        user.set_password(password)
        user.save()
        return user
    
class BaseUserSerializer(ModelSerializer):

    phone_number = PhoneNumberField(blank=False)

    class Meta:
        model = BaseUser
        fields = ['user', 'phone_number']

    

    