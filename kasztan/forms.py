from .models import *
from django.forms import ModelForm
from django import forms

class FormHome(forms.Form):
	pass


class UploadImagesForms(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = '__all__'

class LoginForm(forms.Form):
    login = forms.CharField(max_length=64)
    hasło = forms.CharField(max_length=64, widget=forms.PasswordInput)

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']