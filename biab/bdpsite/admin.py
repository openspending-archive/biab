from django.contrib import admin
from bdpsite.models import Project, DataPackage, Dataset

# Register your models here.
admin.site.register(Project)
admin.site.register(DataPackage)
admin.site.register(Dataset)
