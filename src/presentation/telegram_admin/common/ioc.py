from abc import ABC, abstractmethod

from src.application.interactors.user.create_user.dto import CreateUserDTO, CreateUserResultDTO


class TelegramAdminIoC(ABC):

    @abstractmethod
    async def create_user(self, data: CreateUserDTO) -> CreateUserResultDTO:
        raise NotImplementedError