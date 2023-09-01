from typing import Protocol

from src.application.common.protocols.task_queue import atomacity
from src.application.common.protocols.task_queue import confirmation


class DatabaseGateway(
    atomacity.SupportsCommit,
    confirmation.SupportsEnqueueSendConfirmationEmailTask,
    Protocol
):
    ...