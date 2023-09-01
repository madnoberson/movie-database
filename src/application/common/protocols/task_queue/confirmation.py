from abc import abstractmethod
from typing import Protocol


class SupportsEnqueueSendConfirmationEmailTask(Protocol):

    @abstractmethod
    async def enqueue_send_confirmation_task(self, email: str) -> None:
        raise NotImplementedError