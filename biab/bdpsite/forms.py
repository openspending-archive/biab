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
        fields = ['title', 'slug', 'description', 'featured_viz']
    def __init__(self, *args, **kwargs):
        project = kwargs.get("instance", None)
        super(ProjectForm,self).__init__(*args,**kwargs)
        if project:
            self.fields["featured_viz"].queryset = Visualization.objects.filter(dataset__project__id = project.id)

class CreateForm(forms.Form):
    url = forms.URLField()
    auto_upload = forms.BooleanField(label="Automatically upload datasets?",required=False,initial=True)

class AddDatasetForm(forms.Form):
    slug = forms.SlugField()

class VisualizationForm(forms.ModelForm):
    class Meta:
        model = Visualization
        fields= ['dataset', 'drilldowns', 'cuts', 'type', 'description']
#    def __init__(self, *args, **kwargs):
#        project = kwargs.get("instance", None)
#        super(VisualizationForm, self).__init__(*args, **kwargs)
#        if project:
#            self.fields["dataset"] = forms.ModelChoiceField(
#                queryset = Dataset.objects.filter(project = project).exclude(openspending__isnull=True).exclude(openspending__exact=''))
#                to_field_name = "openspending")