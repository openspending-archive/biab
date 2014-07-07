# Budget in a Box

Budget in a Box is a Django webapp for generating nice budget and spending visualization
sites automatically from Budget Data Packages. Simply point BiaB at the URL of a valid BDP dataset
and BiaB will create a site with rich visualization views of the data. New BDPs can be added to
the site at any time.

*This is a prototype release with basic functionality, to be presented at OKFest 2014.
As of the writing of this README, literally no functionality has been implemented.*

## Configuration

The webapp is configured via environment variables:

* ``OPENSPENDING_API_KEY`` sets the access key for OpenSpending uploading
* ``AWS_ACCESS_KEY_ID`` sets the access key id for S3
* ``AWS_SECRET_ACCESS_KEY`` sets the secret access key (sshh... don't tell anyone)
* ``BIAB_S3_BUCKET`` sets the bucket name where all the CSV files and buckets will be stored
* ``BIAB_S3_HTTP`` sets the URL for the HTTP fron of the S3 bucket. This is needed to serve the budget data packages from the web interface
* ``BIAB_S3_CSV_PREFIX`` sets the prefix used in the keys for the CSV files on S3. Default is *csv/*.
* ``BIAB_S3_MODEL_PREFIX`` sets the prefix used in the keys for the OpenSpending model metadata files. The metadata files will stored at {THIS PREFIX}{DATASET NAME}.json. Default is *bdp/*.


### Setting up a development instance

Create a virtualenv

run 

```
pip install -r requirements.dev.txt
```

Initialize the database
```
DATABASE_URL=sqlite:///biab/biab.sqlite python biab/manage.py syncdb
DATABASE_URL=sqlite:///biab/biab.sqlite python biab/manage.py migrate
```

now start the instance with

```
DATABASE_URL=sqlite:///biab.sqlite honcho start
```
