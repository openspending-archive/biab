from __future__ import absolute_import
from celery import shared_task
from utils.bdp import BDP
import utils.osupload as osu
import utils.s3 as s3

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