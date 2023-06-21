from dataclasses import dataclass
from uuid import UUID
from typing import Literal, Union, Mapping, Iterable
from datetime import datetime, timedelta

from jose import jwt, JWTError

from src.presentation.api.authenticator import ApiAuthenticator
from src.domain.models.user.value_objects import UserId


Algorithm = Literal[
    "HS256",
    "HS384",
    "HS512",
    "RS256",
    "RS384",
    "RS512",
]
Serializable = Union[
    str,
    int,
    float,
    Mapping,
    Iterable
]


class AuthenticationError(Exception):
    ...


@dataclass(frozen=True, slots=True)
class ApiAuthenticatorImpl(ApiAuthenticator):

    secret: str
    access_token_expires: timedelta
    refresh_token_expires: timedelta
    algorithm: Algorithm

    def create_access_token(
        self,
        user_id: UUID
    ) -> str:
        token = self._create_token(
            sub=user_id.hex,
            expires=self.access_token_expires
        )
        return token
    
    def create_refresh_token(
        self,
        user_id: UUID
    ) -> str:
        token = self._create_token(
            sub=user_id.hex,
            expires=self.refresh_token_expires
        )
        return token

    def update_refresh_token(
        self,
        refresh_token: str
    ) -> str:
        payload = jwt.decode(
            token=refresh_token,
            key=self.secret,
            algorithms=self.algorithm,
            options={"verify_exp": False}
        )
        token = self._create_token(
            sub=payload.get("sub"),
            expires=self.refresh_token_expires
        )
        return token
    
    def validate_access_token(
        self,
        access_token: str
    ):
        try:
            payload = jwt.decode(
                token=access_token,
                key=self.secret,
                algorithms=self.algorithm
            )
        except JWTError:
            raise AuthenticationError
        
        return payload.get("sub")
    
    def _create_token(
        self,
        sub: Serializable,
        expires: datetime
    ) -> str:
        expires_ = (
            datetime.utcnow() +
            expires
        )
        payload = {
            "sub": sub,
            "exp": expires_
        }
        token = jwt.encode(
            claims=payload,
            key=self.secret,
            algorithm=self.algorithm
        )

        return token