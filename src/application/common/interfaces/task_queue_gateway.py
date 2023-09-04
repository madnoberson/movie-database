from typing import Protocol

from src.application.common.protocols.task_queue import atomacity
from src.application.common.protocols.task_queue import emails
from src.application.common.protocols.task_queue import person


class DatabaseGateway(
    atomacity.SupportsCommit,

    emails.SupportsEnqueueSendConfirmationEmailTask,
    emails.SupportsEnqueueSendGreetingEmailTask,
    emails.SupportsEnqueueSendUpdateEmailConfirmationEmailTask,
    emails.SupportsEnqueueSendPasswordUpdatedEmailTask,

    person.SupportsEnqueueFillPersonDataTask,

    Protocol
):
    ...