from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField
from django.forms import ModelForm
from bdpsite.models import *
from django import forms

class CaptchaUserCreationForm(UserCreationForm):
   recaptcha = ReCaptchaField()

class DatasetForm(ModelForm):
    granularity = forms.ChoiceField(choices=[("aggregated","aggregated"),("transactional","transactional")])
    type = forms.ChoiceField(choices=[("expenditure","expenditure"),("revenue","revenue")])
    status = forms.ChoiceField(choices=[("proposed","proposed"),("approved","approved"),
                                        ("adjusted","adjusted"),("executed","executed")])
    class Meta:
        model = Dataset
        fields = ['name', 'description',
                  'currency','dateLastUpdated','datePublished',
                  'fiscalYear','granularity', 'type', 'status']

class DataPackageForm(ModelForm):   
    class Meta:
        model = DataPackage
        fields = ['name', 'slug']

class ProjectForm(ModelForm):
    logo = forms.ImageField(required=False)
    class Meta:
        model = Project
        fields = ['title', 'slug', 'description', 'featured_viz', 'logo_url']
    def __init__(self, *args, **kwargs):
        project = kwargs.get("instance", None)
        super(ProjectForm,self).__init__(*args,**kwargs)
#        self.fields["logo_url"].widget.attrs["readonly"] = "readonly"
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