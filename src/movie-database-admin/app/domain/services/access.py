from app.domain.models.access_policy import AccessPolicy
from app.domain.constants import SuperUserPermissionEnum
from app.domain.exceptions.access import AccessDeniedError


class AccessService:

    def ensure_can_create_superuser(
        self, access_policy: AccessPolicy
    ) -> None:
        if (
            not SuperUserPermissionEnum.SUPERUSERS
            in access_policy.permissions
        ):
            raise AccessDeniedError()