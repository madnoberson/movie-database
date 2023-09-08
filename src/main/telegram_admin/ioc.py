from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncIterator

from src.application.interactors.user.create_user.dto import CreateUserDTO, CreateUserResultDTO
from src.application.interactors.user.create_user.interactor import CreateUser
from src.application.common.interfaces.database_gateway import DatabaseGateway
from src.application.common.interfaces.password_encoder import PasswordEncoder
from src.presentation.telegram_admin.common.ioc import TelegramAdminIoC


class DatabaseGatewayFactory(ABC):

    @abstractmethod
    async def create_gateway(self) -> AsyncIterator[DatabaseGateway]:
        raise NotImplementedError
    

@dataclass(frozen=True, slots=True)
class TelegramAdminIoCImpl(TelegramAdminIoC):

    db_gateway_factory: DatabaseGatewayFactory
    password_encoder: PasswordEncoder

    async def create_user(self, data: CreateUserDTO) -> CreateUserResultDTO:
        async with self.db_gateway_factory.create_gateway() as db_gateway:
            create_user = CreateUser(
                db_gateway=db_gateway, password_encoder=self.password_encoder
            )
            return await create_user(data)