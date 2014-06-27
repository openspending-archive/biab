from django.contrib import admin
from bdpsite.models import DataPackage, Dataset

# Register your models here.
admin.site.register(DataPackage)
admin.site.register(Dataset)