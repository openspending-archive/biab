from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField
from django.forms import ModelForm
from bdpsite.models import *

class CaptchaUserCreationForm(UserCreationForm):
   recaptcha = ReCaptchaField()

class DataPackageForm(ModelForm):   
    class Meta:
        model = DataPackage
        fields = ['name', 'slug']
