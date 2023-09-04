from typing import Protocol

from src.application.common.protocols.database import atomacity as atomacity_db
from src.application.common.protocols.database import person as person_db
from src.application.common.protocols.cachebase import atomacity as atomacity_cb
from src.application.common.protocols.cachebase import person as person_cb
from src.application.common.protocols.filebase import atomacity as atomacity_fb
from src.application.common.protocols.filebase import person as person_fb


class DatabaseGateway(
    atomacity_db.SupportsCommit,
    person_db.SupportsGetPerson,
    person_db.SupportsUpdatePerson,
    Protocol
):
    ...


class CachebaseGateway(
    atomacity_cb.SupportsCommit,
    person_cb.SupportsGetPerson,
    person_cb.SupportsSavePerson,
    person_cb.SupportsUpdatePerson,
    Protocol
):
    ...


class FilebaseGateway(
    atomacity_fb.SupportsCommit,
    person_fb.SupportsUpdatePersonAvatar,
    Protocol
):
    ...