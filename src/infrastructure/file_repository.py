from dataclasses import dataclass
from typing import IO

from boto3_type_annotations.s3 import Client

from src.application.common.file_repository import FileRepostory


ObjectStorageClient = Client


@dataclass(frozen=True, slots=True)
class YandexOSFileRepository(FileRepostory):

    bucket_name: str
    object_storage: ObjectStorageClient

    def add_image(self, image: IO, key: str) -> None:
        self.object_storage.upload_fileobj(
            Fileobj=image,
            Bucket=self.bucket_name,
            Key=key
        )