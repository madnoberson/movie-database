from typing import Protocol

from src.application.common.protocols.task_queue import atomacity
from src.application.common.protocols.task_queue import emails


class DatabaseGateway(
    atomacity.SupportsCommit,
    emails.SupportsEnqueueSendConfirmationEmailTask,
    emails.SupportsEnqueueSendGreetingEmailTask,
    Protocol
):
    ...