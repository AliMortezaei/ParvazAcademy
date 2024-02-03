from storages.backends.s3boto3 import S3Boto3Storage
from core import settings


class ImageMediaStorage(S3Boto3Storage):
    location = settings.PUBLIC_MEDIA_LOCATION
    default_acl = 'public-read'
    file_overwrite = False