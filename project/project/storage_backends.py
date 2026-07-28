"""
Custom storage backends for Cloudflare R2.
"""
from storages.backends.s3boto3 import S3Boto3Storage


class R2MediaStorage(S3Boto3Storage):
    """Cloudflare R2 storage backend for Media files."""
    location = 'media'
    default_acl = None
    file_overwrite = False
    querystring_auth = False
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from botocore.config import Config
        self.config = Config(
            signature_version='s3v4',
            connect_timeout=15,
            read_timeout=30,
            retries={'max_attempts': 3}
        )

    def exists(self, name):
        try:
            return super().exists(name)
        except Exception:
            return False

    def get_modified_time(self, name):
        try:
            return super().get_modified_time(name)
        except Exception:
            return None


class R2StaticStorage(S3Boto3Storage):
    """Cloudflare R2 storage backend for Static files."""
    location = 'static'
    default_acl = None
    file_overwrite = True
    querystring_auth = False
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from botocore.config import Config
        self.config = Config(
            signature_version='s3v4',
            connect_timeout=15,
            read_timeout=30,
            retries={'max_attempts': 3}
        )

    def exists(self, name):
        try:
            return super().exists(name)
        except Exception:
            return False

    def get_modified_time(self, name):
        try:
            return super().get_modified_time(name)
        except Exception:
            return None
