from abc import ABC, abstractmethod

from src.application.interactors.user.create_user.dto import CreateUserDTO, CreateUserResultDTO
from src.application.interactors.queries.user.check_email_exists.dto import CheckEmailExistsDTO, CheckEmailExistsResultDTO


class TelegramAdminIoC(ABC):

    @abstractmethod
    async def create_user(self, data: CreateUserDTO) -> CreateUserResultDTO:
        raise NotImplementedError
    
    @abstractmethod
    async def check_email_exists(self, data: CheckEmailExistsDTO) -> CheckEmailExistsResultDTO:
        raise NotImplementedError