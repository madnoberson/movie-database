from typing import Annotated

from boto3 import Session
from boto3_type_annotations.s3 import Client

from src.domain.models.movie.value_objects import MoviePosterKey
from src.application.common.interfaces.filebase_gateway import (
    FilebaseGateway
)


Boto3S3Session = Session


class YandexOSFilebaseGateway(FilebaseGateway):

    image_bucket: str
    boto3_client: Annotated[Client, Boto3S3Session]

    def save_movie_poster(
        self,
        poster: bytes,
        key: MoviePosterKey
    ) -> None:
        self.boto3_client.upload_fileobj(
            Fileobj=poster,
            Bucket=self.image_bucket,
            Key=key
        )