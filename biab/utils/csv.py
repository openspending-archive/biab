# -*- coding: utf-8 -*-

import urllib
import unicodecsv as csv
import StringIO

class DatasetCSV(object):
    """
    BDP datasets are CSV files.

    This class wraps a CSV file accessible at a URL.

    Data is stored internally as a sequence of dictionaries
    in csv.DictReader format.

    Headers are stored as a separate list.
    """
    def __init__(self, csvurl, *args, **kwargs):
        self.url = csvurl
        # Get the data and set self.rows and self.headers
        self._load_data()

    def _load_data(self):
        """
        Grabs the CSV rows from the stored URL and saves them.

        This assumes a CSV whose first row contains headers.
        """

        # Get the header
        csvfile = urllib.urlopen(self.url)
        reader = csv.reader(csvfile)
        self.headers = reader.next()
        csvfile.close()

        # Create the headers dictionary row,
        # necessary for serializing the data
        headers_dict = {}
        for header in self.headers:
            headers_dict[header] = header
        self.headers_dict = headers_dict

        # Get the rows
        rows = []
        csvfile = urllib.urlopen(self.url)
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)
        self.rows = rows
        csvfile.close()

    def append_headers(self, headers):
        """
        Update the internal list of headers and header
        dictionary object by adding a list of new headers.
        """

        self.headers = self.headers + headers

        for header in headers:
            self.headers_dict[header] = header

    def append_columns(self, column_names, row_function):
        """
        Adds new columns to the CSV.

        Takes a list of names of the new columns (column_name) and a
        function to apply to each row to yield up the values of those
        columns for the row. (Columns with a constant value can simply
        use functions that return a constant value.)

        Internally, this method works with DictReader and DictWriter
        objects. The return value of row_function ought to be a dictionary
        that can be merged with the rows from the CSV as rendered
        by DictReader.
        """

        # Insert the new headers
        self.append_headers(column_names)

        # Apply the row function to each row, and
        # update the row with the result (n.b. rows are mutable!)
        for row in self.rows:
            row.update(row_function(row))

    def rename_column(self, column_name, new_name):
        """
        Renames a column.

        This has to update the internal list of headers as well
        as changing the content of every row.
        """
        hs = self.headers
        if column_name not in hs:
            return False
        i = hs.index(column_name)
        self.headers = hs[:i] + [new_name] + hs[(i+1):]
        self.headers_dict.pop(column_name)
        self.headers_dict[new_name] = new_name
        for row in self.rows:
            row[new_name] = row.pop(column_name)

    def serialize(self):
        """
        Returns the data in a string, suitable for writing to S3.
        """
        output = StringIO.StringIO()
        writer = csv.DictWriter(output, self.headers)
        data = [self.headers_dict] + self.rows
        writer.writerows(data)
        return output.getvalue()