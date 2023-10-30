from uuid import UUID

from redis.asyncio import Redis

from app.domain.models.access_policy import AccessPolicy
from app.domain.models.superuser import SuperUserPermissionEnum


class AccessPolicyDoesNotExistError(Exception):
    ...


class AccessPolicyGateway:

    def __init__(self, connection: Redis) -> None:
        self.connection = connection
    
    async def save_access_policy(self, access_policy: AccessPolicy) -> None:
        """Deletes old access policy and saves new one"""
        async with self.connection.pipeline() as pipeline:
            await pipeline.delete(
                f"permissions:superuser_id:{access_policy.superuser_id.hex}"
            )
            await pipeline.rpush(
                f"permissions:superuser_id:{access_policy.superuser_id.hex}",
                *[permission.value for permission in access_policy.permissions]
            )
            await pipeline.hset(
                f"access_policies:superuser_id:{access_policy.superuser_id.hex}",
                mapping={"is_active": int(access_policy.is_active)}
            )
            await pipeline.execute()
    
    async def get_access_policy(self, superuser_id: UUID) -> AccessPolicy:
        """
        Returns superuser access policy by `superuser_id` if exists, otherwise
        raises `AccessPolicyDoesNotExistError`
        """
        data = await self.connection.hgetall(
            f"access_policies:superuser_id:{superuser_id.hex}"
        )
        permissions = await self.connection.lrange(
            name=f"permissions:superuser_id:{superuser_id.hex}",
            start=0, end=-1
        )
        return AccessPolicy(
            superuser_id=superuser_id, is_active=bool(data["is_active"]),
            permissions=[
                SuperUserPermissionEnum(int(permission)) for permission in permissions
            ]
        )
