from dataclasses import dataclass
from typing import Annotated
from io import BytesIO

from boto3 import Session
from boto3_type_annotations.s3 import Client

from src.domain.models.movie.value_objects import MoviePosterKey
from src.application.common.interfaces.filebase_gateway import (
    FilebaseGateway
)


Boto3S3Session = Session


@dataclass(frozen=True, slots=True)
class YandexOSFilebaseGateway(FilebaseGateway):

    image_bucket: str
    boto3_client: Annotated[Client, Boto3S3Session]

    def save_movie_poster(
        self,
        poster: BytesIO,
        key: MoviePosterKey
    ) -> None:
        self.boto3_client.upload_fileobj(
            Fileobj=poster,
            Bucket=self.image_bucket,
            Key=key.value,
            ExtraArgs={"ContentType":"image/png"}
        )
    
    def remove_movie_poster(
        self,
        key: MoviePosterKey
    ) -> None:
        self.boto3_client.delete_object(
            Bucket=self.image_bucket,
            Key=key
        )
        