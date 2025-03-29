from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


def remove_http(url: str) -> str:
    if url.startswith("http://"):
        return url[7:]
    elif url.startswith("https://"):
        return url[8:]
    return url


class MinioBerkehPhotosStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BERKEH_PHOTOS_BUCKET_NAME
    custom_domain = f"{remove_http(settings.AWS_S3_ENDPOINT_URL)}/{settings.AWS_STORAGE_BERKEH_PHOTOS_BUCKET_NAME}"
