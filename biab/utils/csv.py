# -*- coding: utf-8 -*-

from django.conf import settings
import urllib
import unicodecsv as csv

class DatasetCSV(object):
    """
    BDP datasets are CSV files.

    This class wraps a CSV file accessible at a URL.
    """
    def __init__(self, csvurl, *args, **kwargs):
        self.url = csvurl
        self.rows = self._get_rows()
        self.headers = self._get_headers()

    def _get_rows(self):
        """
        Grabs the CSV rows from the stored URL and saves them.
        """
        rows = []
        with urllib.urlopen(self.csv_url) as csvfile:
            reader = csv.reader(csvfile)
            reader.next()
            for row in reader:
                rows.append(row)
        return rows

    def _get_headers(self):
        with urllib.urlopen(self.csv_url) as csvfile:
            return csv.reader(csvfile).next()