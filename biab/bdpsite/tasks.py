from __future__ import absolute_import
from celery import shared_task
from utils.bdp import BDP
import utils.osupload as osu
import utils.s3 as s3
from django.utils.text import slugify
import dateutil.parser
from urlparse import urljoin

from bdpsite.models import *

from utils.osupload import process_resource, model, os_load
from utils.csv import DatasetCSV
from utils.s3 import put_dataset, put_model

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
#    d.slug = slugify(d.name)
    d.path = metadata_url
    d.save()

    # Create model instances for the bdp's resources.
    for resource in d_obj.metadata["resources"]:
        create_dataset.delay(project, d, resource)
    return True

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
    return True

def reconstruct_resource(dataset, preprocessed=False):
    my_url = dataset.path
    if preprocessed:
        my_url = dataset.preprocessed
    url = urljoin(dataset.datapackage.path, my_url)
    return {
        "data": DatasetCSV(url),
        "metadata": {
            "path": dataset.path,
            "name": dataset.name,

            "currency": dataset.currency,
            "dateLastUpdated": dataset.dateLastUpdated,
            "datePublished": dataset.datePublished,
            "fiscalYear": dataset.fiscalYear,
            "granularity": dataset.granularity,
            "status": dataset.status,
            "type": dataset.type
        }
    }

@shared_task
def preprocess_dataset(id):
    dataset = Dataset.objects.get(id=id)
    resource = reconstruct_resource(dataset)
    process_resource(resource)
    dataset.preprocessed = put_dataset(dataset.name, resource["data"].serialize())
    dataset.save()
    return True

@shared_task
def generate_model(id):
    dataset = Dataset.objects.get(id=id)
    resource = reconstruct_resource(dataset, preprocessed=True)
    dataset_model = model(resource)
    # now do something with dataset_model
    # ... like post it on S3
    # ... and store the result
    dataset.datamodel = put_model(dataset.name, dataset_model)
    dataset.save()
    # dataset.datamodel = s3_url
    return True

@shared_task
def osload(id):
    dataset = Dataset.objects.get(id=id)
    if dataset.preprocessed is None or dataset.datamodel is None:
        return False
    response_json = os_load(dataset.preprocessed, dataset.datamodel)
    dataset.openspending = response_json["html_url"]
    dataset.save()
    return True

@shared_task
def process_and_load(dataset):
    """
    Checks to make sure the dataset has associated `preprocessed`
    and `datamodel` attributes. If not, creates them
    (synchronously, because they depend on one another).

    Once everything is in the clear, posts the result on OpenSpending.
    """
    if dataset.preprocessed is None:
        preprocess_dataset.delay(dataset).get()
    if dataset.datasetmodel is None:
        generate_model.delay(dataset).get()
    return osload.delay(dataset)