from django.contrib import admin
from bdpsite.models import *

# Register your models here.
admin.site.register(Project)
admin.site.register(DataPackage)
admin.site.register(Dataset)
admin.site.register(Visualization)