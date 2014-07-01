from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField
from django.forms import ModelForm
from bdpsite.models import *
from django import forms

class CaptchaUserCreationForm(UserCreationForm):
   recaptcha = ReCaptchaField()

class DataPackageForm(ModelForm):   
    class Meta:
        model = DataPackage
        fields = ['name', 'slug']

class ProjectForm(ModelForm):   
    class Meta:
        model = Project
        fields = ['title', 'slug', 'description']

class CreateForm(forms.Form):
    url = forms.URLField()

