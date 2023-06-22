import hashlib

import cloudinary
import cloudinary.uploader

from src.conf.config import settings, config_cloudinary


class UploadService:
    config_cloudinary()

    @staticmethod
    def create_name_avatar(email: str, prefix: str):
        config_cloudinary()
        name = hashlib.sha256(email.encode()).hexdigest()[:12]
        return f"{prefix}/{name}"

    @staticmethod
    def upload(file, public_id):
        config_cloudinary()
        r = cloudinary.uploader.upload(file, public_id=public_id, overwrite=True)
        return r

    @staticmethod
    def get_url_avatar(public_id, version):
        config_cloudinary()
        src_url = cloudinary.CloudinaryImage(public_id).build_url(width=250, height=250, crop='fill', version=version)
        return src_url
    