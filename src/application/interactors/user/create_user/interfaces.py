from typing import Protocol

from src.application.common.protocols.database import atomacity as atomacity_db
from src.application.common.protocols.database import user as user_db
from src.application.common.protocols.cachebase import atomacity as atomacity_cb
from src.application.common.protocols.cachebase import user as user_cb
from src.application.common.protocols.task_queue import atomacity as atomacity_tq
from src.application.common.protocols.task_queue import confirmation as confirmation_tq
from src.application.common.interfaces.password_encoder import PasswordEncoder


class DatabaseGateway(
    atomacity_db.SupportsCommit,
    user_db.SupportsGetUser,
    user_db.SupportsSaveUser,
    Protocol
):
    ...


class CachebaseGateway(
    atomacity_cb.SupportsCommit,
    user_cb.SupportsGetUser,
    user_cb.SupportsSaveUser,
    Protocol
):
    ...


class TaskQueueGateway(
    atomacity_tq.SupportsCommit,
    confirmation_tq.SupportsEnqueueSendConfirmationEmailTask,
    Protocol
):
    ...