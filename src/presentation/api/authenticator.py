from abc import ABC, abstractmethod
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Cookie, HTTPException


class AuthenticationError(Exception):
    ...


class ApiAuthenticator(ABC):

    @abstractmethod
    def create_access_token(
        self,
        user_id: UUID
    ) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def validate_access_token(
        self,
        access_token: str
    ) -> UUID:
        raise NotImplementedError


def get_user_id(
    authenticator: Annotated[ApiAuthenticator, Depends()],
    access_token: str | None = Cookie(None),
) -> UUID | None:
    if not access_token:
        return None

    try:
        user_id = authenticator.validate_access_token(
            access_token=access_token
        )
    except AuthenticationError:
        raise HTTPException(401)

    return user_id