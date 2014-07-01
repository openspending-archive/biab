from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True,blank=True)
    creator = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.title

class DataPackage(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return self.name

class Dataset(models.Model):
    # the BDP that contains the dataset
    datapackage = models.ForeignKey(DataPackage,null=True,blank=True)
    project = models.ForeignKey(Project)

    # stuff from BDP resource metadata
    path = models.CharField(max_length=256,null=True,blank=True)
    name = models.CharField(max_length=256)
    currency = models.CharField(max_length=256)
    dateLastUpdated = models.DateTimeField()
    datePublished = models.DateTimeField()
    fiscalYear = models.DateTimeField(null=True,blank=True)
    granularity = models.CharField(max_length=256,null=True, blank=True)
    status = models.CharField(max_length=256,null=True, blank=True)
    type = models.CharField(max_length=256)
    description = models.TextField(null=True,blank=True)

    def __unicode__(self):
        if self.datapackage:
            return self.name + " (in " + \
                self.datapackage.name + ")"
        else:
            return self.name

class Visualization(models.Model):
    dataset = models.ForeignKey(Dataset)
