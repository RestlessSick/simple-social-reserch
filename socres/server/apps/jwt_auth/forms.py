from django import forms
from phonenumber_field import formfields
from phonenumber_field import widgets as phonewidgets

from django_bootstrap5 import widgets as b5

class RegisterForm(forms.Form):

    phone = formfields.PhoneNumberField(region='RU', empty_value=False, widget=phonewidgets.RegionalPhoneNumberWidget(region='RU'))
    password = forms.CharField(empty_value=False, widget=b5.PasswordInput)

class LoginForm(forms.Form):
    phone = formfields.PhoneNumberField(region='RU', empty_value=False, widget=phonewidgets.RegionalPhoneNumberWidget(region='RU'))
    password = forms.CharField(empty_value=False, widget=b5.PasswordInput)
