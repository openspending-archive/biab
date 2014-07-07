from django.conf import settings
from boto import connect_s3
import uuid

def get_bucket():    
    """
    Connect to s3 with credentials provided by the application
    and return the bucket as configured by the app.
    """
    bucket_name = settings.S3_BUCKET #app.config['S3_BUCKET']
    if bucket_name is None:
        raise EnvironmentError('Application is improperly configured: S3_BUCKET not set')

    connection = connect_s3()
    return connection.get_bucket(bucket_name)

def put_content(key_name, content, content_type=None):
    """
    Put a string onto s3 at the given key name.
    The bucket comes from the app configuration.
    Returns a public URL for the new file.
    """

    bucket = get_bucket()
    key = bucket.new_key(key_name)
    if content_type:
        key.set_metadata('Content-Type', content_type)
    key.set_contents_from_string(content)
    key.set_acl('public-read')
    return key.generate_url(expires_in=0, query_auth=False)

def generate_key(filename, prefix=''):
    """
    Generate a key name for the filename and a prefix
    """
    return '{prefix}{filename}'.format(prefix=prefix, filename=filename)

def uuidize(name):
    return name + "-" + str(uuid.uuid4());

def put_dataset(name, content):
    """
    Convenience function to post a CSV dataset.
    """
    key = generate_key(uuidize(name) + ".csv", settings.S3_CSV_PREFIX)
    return put_content(key, content, content_type="application/json")

def put_model(name, content):
    """
    Convenience function to post an OS model.
    """
    key = generate_key(uuidize(name) + ".json", settings.S3_MODEL_PREFIX)
    return put_content(key, content, content_type="application/json")