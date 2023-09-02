from abc import abstractmethod
from typing import Protocol
from uuid import UUID


class SupportsEnqueueSendConfirmationEmailTask(Protocol):

    @abstractmethod
    async def enqueue_send_confirmation_email_task(self, email: str) -> None:
        raise NotImplementedError


class SupportsEnqueueSendGreetingEmailTask(Protocol):

    @abstractmethod
    async def enqueue_send_greeting_email_task(self, user_id: UUID) -> None:
        raise NotImplementedError


class SupportsEnqueueSendUpdateEmailConfirmationEmailTask(Protocol):

    @abstractmethod
    async def enqueue_send_update_email_confirmation_email_task(self, email: str) -> None:
        raise NotImplementedError
