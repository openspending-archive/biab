from __future__ import absolute_import
from celery import shared_task
from utils.bdp import BDP
import utils.osupload as osu
import utils.s3 as s3
from django.utils.text import slugify
import dateutil.parser

from bdpsite.models import *

@shared_task
def add(x, y):
    return x + y

@shared_task
def upload_bdp(metadata_url):
    bdp = BDP(metadata_url)
    for resource in bdp.resources:
        # Preprocess the CSV
        osu.process_resource(resource)
        # Create the model for the CSV
        model = osu.model(resource)
        # Post the CSV and model on S3
        name = resource["metadata"]["name"]
        data_url = s3.put_dataset(resource["data"].serialize(), name)
        model_url = s3.put_model(model, name)
        # Call the OS loading API on the result
        osu.os_load(data_url, model_url)

@shared_task
def create_bdp(project, metadata_url):
    # Create an internal representation.
    # This loads the metadata.
    d_obj = BDP(metadata_url)

    # Create a model instance for the new bdp.
    d = DataPackage()
    d.project = project
    d.name = d_obj.metadata["name"]
    d.slug = slugify(d.name)
    d.path = metadata_url
    d.save()

    # Create model instances for the bdp's resources.
    for resource in d_obj.metadata["resources"]:
        create_dataset.delay(project, d, resource)
    return None

@shared_task
def create_dataset(project, bdp, resource):
    d = Dataset()
    d.datapackage = bdp
    d.project = project

    d.path = resource["path"]
    d.name = resource["name"]
    d.currency = resource["currency"]
    d.dateLastUpdated = dateutil.parser.parse(resource["dateLastUpdated"])
    d.datePublished = dateutil.parser.parse(resource["datePublished"])
    d.fiscalYear = dateutil.parser.parse(resource["fiscalYear"])
    d.granularity = resource["granularity"]
    d.status = resource["status"]
    d.type = resource["type"]

    d.description = resource.get("description", "")

    d.save()
    return None