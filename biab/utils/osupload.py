# -*- coding: utf-8 -*-

from django.conf import settings
from utils.bdp import BDP
from functools import reduce
from copy import copy
from urllib2 import urlopen, urlencode, Request
import os
import json

# Helper dictionaries for looking up values needed to construct OS
# models.

# Map from (processed) field names to mapping objects.
# Used to construct the model mapping for OS uploading.
with open(os.path.join(settings.RESOURCES, "model-map.json")) as mmf:
    model_map = json.loads(mmf.read())

# List of lists of field names that can be bundled
# together as compound dimensions.
bundleable = [
    ["admin","adminID","adminOrgID"],
    ["economic","economicID"],
    ["functional","functionalID"],
    ["fund","fundID"],
    ["program","programID"],
    ["project","projectID"],
    ["purchaserID","purchaserOrgID"]
]


# The expected workflow with these functions is:
# - create a BDP object using utils.bdp
# - call process_resource() on each resource in the BDP
# - write each processed resource to S3
# - generate model for each processed resource with model()
# - write each generated model to S3
# - post the processed CSV and metadata to OS with an API call

def os_upload(csv_url,metadata_url):
    """
    Makes a Loading API call using the supplied URLs and the API
    key supplied by the app configuration.
    """
    url = "https://openspending.org/api/2/new"
    header = {
        "Authorization": "ApiKey " + settings.OPENSPENDING_API_KEY
    }
    values = {
        "csv_file": csv_url,
        "metadata": metadata_url
    }
    data = urlencode(values)
    request = Request(url, data, header)
    response = urlopen(request)
    return response

def process_resource(resource, metadata):
    """
    Takes a DatasetCSV object and a (resource) metadata object.

    Updates the object by calling preprocessing methods on it.

    The resulting object will be ready to write to S3 by means
    of its serialize() method. (It will, however, no longer be
    a valid BDP dataset, or at least it will no longer match its
    metadata!)
    """
    headers = resource.headers

    # split out COFOG column
    if cofog_pred(headers):
        resource.append_columns(
            ["cofog1","cofog2","cofog3"],
            split_cofog)

    # split out GFSM exp column
    if gfsm_expenditure_pred(headers):
        resource.append_columns(
            ["gfsmExpenditure1",
             "gfsmExpenditure2",
             "gfsmExpenditure3",
             "gfsmExpenditure4",
             "gfsmExpenditure5"],
             split_gfsm_expenditure)

    # split out GFSM rev column
    if gfsm_revenue_pred(headers):
        resource.append_columns(
            ["gfsmRevenue1",
             "gfsmRevenue2",
             "gfsmRevenue3",
             "gfsmRevenue4"],
             split_gfsm_revenue)

    # does the dataset have a date column? no?
    # no problem! just use its fiscal year...
    if "date" not in headers:
        resource.append_columns(["date"],append_date(metadata["fiscalYear"]))

    return True

def model(resource, metadata):
    """
    Returns (in string form) the JSON model object that can be
    used to update the resource to OpenSpending.
    """
    mapping_fields = model_fields(resource)
    mapping = {}
    for field in mapping_fields:
        mapping[field] = mapping_field(field)
    dataset = dataset_attribute(metadata)
    model = {
        "mapping": mapping,
        "dataset": dataset
    }
    return json.dumps(model)

def mapping_field(field):
    """
    Returns a mapping object for the field name.

    If it is a known field (i.e. it is in model-map.json),
    then the predefined mapping object is returned.

    Otherwise an uninformative default value is returned.
    """
    if field in model_map.keys():
        return model_map[field]
    else:
        return {
            "default_value": "",
            "description": field + " (user field)", 
            "column": field,
            "label": field.capitalize(),
            "datatype": "string",
            "type": "attribute"
        }

def model_fields(resource):
    """
    Returns the processed list of fields that will end up in
    the resource's model file.

    This list of fields bundles together fields that can be
    treated as members of a single compound dimension.
    """
    headers = resource.headers
    return bundle_all(headers, bundleable)

def dataset_attribute(metadata):
    """
    Returns the `dataset` attribute that can be extracted from a resource's metadata.
    """
    return {
            "name": metadata["name"],
            "currency": metadata["currency"]
        }

def bundle(headers, to_bundle):
    """
    Takes a headers list and a list of headers to be bundled
    together.

    Returns a new headers list with the to-be-bundled items
    removed and the bundled item added.
    """

    items_present = filter(lambda h: h in headers, to_bundle)
    if len(items_present) == 0:
        return headers

    result = copy(headers)
    for item in items_present:
        result.remove(item)

    result.append(" + ".join(items_present))
    return result

def bundle_all(headers, bundles):
    """
    Applies bundle() with a whole list of to_bundle items.
    """
    return reduce(bundle,bundles,headers)

def cofog_pred(headers):
    """
    Checks if a list of headers is such that `cofog` should
    be split out.
    """
    return not ("cofog" not in headers
        or "cofog1" in headers
        or "cofog2" in headers
        or "cofog3" in headers)

def gfsm_expenditure_pred(headers):
    """
    Checks if a list of headers is such that `gfsmExpenditure`
    should be split out.
    """
    return not ("gfsmExpenditure" not in headers
        or "gfsmExpenditure1" in headers
        or "gfsmExpenditure2" in headers
        or "gfsmExpenditure3" in headers
        or "gfsmExpenditure4" in headers
        or "gfsmExpenditure5" in headers)

def gfsm_revenue_pred(headers):
    """
    Checks if a list of headers is such that `gfsmRevenue`
    should be split out.
    """
    return not ("gfsmRevenue" not in headers
        or "gfsmRevenue1" in headers
        or "gfsmRevenue2" in headers
        or "gfsmRevenue3" in headers
        or "gfsmRevenue4" in headers)

def split_cofog(row):
    """
    Takes a DictReader row dictionary and returns a dictionary
    that splits the row's "cofog" value into three columns.
    """
    cofog_value = row["cofog"]
    cofog_list = cofog_value.split(".")
    length = len(cofog_list)
    # make sure the list isn't too long
    if length > 3:
        raise ValueError("Input COFOG value has too many sublevels (" + str(length) + ")")
    # pad the list if it's too short
    if length < 3:
        for _ in range(3 - length):
            cofog_list.append("")
    # create the result dictionary
    result = {}
    for i in range(3):
        result["cofog" + str(i+1)] = cofog_list[i]
    return result

def split_gfsm(row, type):
    """
    Takes a DictReader row dictionary and returns a dictionary
    that splits the row's "gfsmExpenditure" or "gfsmRevenue",
    given by `type`.
    """
    target = "gfsm" + type
    gfsm_value = row[target]
    gfsm_list = gfsm_value.split('.')
    length = len(gfsm_list)
    if type == "Revenue":
        ideal_length = 5
    else:
        ideal_length = 4
    if length > ideal_length:
        raise ValueError("Input GFSM value has too many sublevels (" + str(length) + ")")
    if length < ideal_length:
        for _ in range(ideal_length - length):
            gfsm_list.append("")
    result = {}
    for i in range(ideal_length):
        result["gfsm" + type + str(i+1)] = gfsm_list[i]
    return result

split_gfsm_expenditure = lambda r: split_gfsm(r, "Expenditure")
split_gfsm_revenue = lambda r: split_gfsm(r, "Revenue")

def append_date(date):
    """
    Returns a parameterized row-modification function that appends a 
    constant year 
    """
    return lambda _: {"date":date}