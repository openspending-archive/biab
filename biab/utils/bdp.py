# -*- coding: utf-8 -*-

from utils.csv import DatasetCSV
import json
import urllib
from urlparse import urljoin

class BDP(object):
    """
    A valid BDP consists of a metadata file and an arbitrary number
    of CSV datasets linked from the metadata file's resources array.
    (This implementation supports arbitrarily many datasets.)
    """

    def __init__(self, metadata_url, *args, **kwargs):
        self.metadata_url = metadata_url

        # Get metadata and initialize:
        #   self.metadata
        self._download_metadata()

        # Download all resources and initialize:
        #   self.resources
        self.resources = []
        self._download_resources()

    def _download_metadata(self):
        """
        Downloads the metadata from the given url.
        """
        metadata_file = urllib.urlopen(self.metadata_url)
        self.metadata = json.loads(metadata_file.read())
        metadata_file.close()

    def _download_resources(self):
        """
        Gets all the resources linked from the metadata.

        This creates an array of DatasetCSV instances in self.resources.
        """

        for resource in self.metadata["resources"]:
            resource_url = urljoin(self.metadata_url, resource["path"])
            self.resources.append(DatasetCSV(resource_url))