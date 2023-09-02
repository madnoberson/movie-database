from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class User:

    id: UUID
    email: str
    username: str
    encoded_password: str
    created_at: datetime
    updated_at: datetime
    is_confirmed: bool
    is_active: bool

    avatar_url: str | None

    @classmethod
    def create(
        cls, user_id: UUID, email: str, username: str,
        encoded_password: str, created_at: str
    ) -> "User":
        return User(
            id=user_id, email=email, username=username,
            encoded_password=encoded_password, created_at=created_at,
            is_confirmed=False, is_active=True, avatar_url=None
        )
    
    def confirm(self) -> None:
        self.is_confirmed = True
    
    def deactivate(self) -> None:
        self.is_active = False
    
    def update_email(self, email: str, updated_at: datetime) -> None:
        self.email = email
        self.updated_at = updated_at

    def update_password(self, encoded_password: str, updated_at: datetime) -> None:
        self.encoded_password = encoded_password
        self.updated_at = updated_at

    def update_username(self, username: str, updated_at: datetime) -> None:
        self.username = username
        self.updated_at = updated_at
    
    def update_avatar(self, avatar_url: str, updated_at: datetime) -> None:
        self.avatar_url = avatar_url
        self.updated_at = updated_at