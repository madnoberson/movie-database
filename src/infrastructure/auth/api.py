from dataclasses import dataclass
from uuid import UUID
from typing import Literal
from datetime import datetime, timedelta

from jose import jwt, JWTError

from src.presentation.api.authenticator import (
    ApiAuthenticator,
    AuthenticationError
)


Algorithm = Literal[
    "HS256",
    "HS384",
    "HS512",
    "RS256",
    "RS384",
    "RS512",
]


@dataclass(frozen=True, slots=True)
class ApiAuthenticatorImpl(ApiAuthenticator):

    secret: str
    access_token_expires: timedelta
    algorithm: Algorithm

    def create_access_token(
        self,
        user_id: UUID
    ) -> str:
        expires = (
            datetime.utcnow() +
            self.access_token_expires
        )
        payload = {
            "sub": user_id.hex,
            "exp": expires
        }
        token = jwt.encode(
            claims=payload,
            key=self.secret,
            algorithm=self.algorithm
        )
        return token
    
    def validate_access_token(
        self,
        access_token: str
    ) -> UUID | None:
        try:
            payload = jwt.decode(
                token=access_token,
                key=self.secret,
                algorithms=self.algorithm
            )
        except JWTError:
            raise AuthenticationError
        
        raw_user_id = payload.get("sub")
        if raw_user_id is None:
            return None
        
        try:
            user_id = UUID(raw_user_id)
        except:
            raise AuthenticationError

        return user_id
