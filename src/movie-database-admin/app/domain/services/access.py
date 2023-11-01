from app.domain.models.access_policy import AccessPolicy
from app.domain.models.superuser import Superuser
from app.domain.models.superuser import SuperUserPermissionEnum
from app.domain.exceptions.access import AccessDeniedError


class AccessService:

    def ensure_can_create_superuser(
        self, access_policy: AccessPolicy
    ) -> None:
        if (
            not access_policy.is_active or
            
            not SuperUserPermissionEnum.SUPERUSERS
            in access_policy.permissions
        ):
            raise AccessDeniedError()
    
    def ensure_can_change_username(
        self, access_policy: AccessPolicy
    ) -> None:
        if (
            not access_policy.is_active or

            not SuperUserPermissionEnum.USERS
            in access_policy.permissions
        ):
            raise AccessDeniedError()
    
    def ensure_can_change_superuser_password(
        self, access_policy: AccessPolicy, superuser: Superuser
    ) -> None:
        if (
            not access_policy.is_active or

            not SuperUserPermissionEnum.SUPERUSERS
            in access_policy.permissions or

            SuperUserPermissionEnum.SUPERUSERS 
            in superuser.permissions
        ):
            raise AccessDeniedError()