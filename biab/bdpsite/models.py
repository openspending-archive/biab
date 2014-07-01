from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DataPackage(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

class Dataset(models.Model):
    # the BDP that contains the dataset
    datapackage = models.ForeignKey(DataPackage)

    # stuff from BDP resource metadata
    path = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    currency = models.CharField(max_length=256)
    dateLastUpdated = models.DateTimeField()
    datePublished = models.DateTimeField()
    fiscalYear = models.DateTimeField()
    granularity = models.CharField(max_length=256)
    status = models.CharField(max_length=256)
    type = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name + " (in " + \
            self.datapackage.name + ")"

class Visualization(models.Model):
    dataset = models.ForeignKey(Dataset)
