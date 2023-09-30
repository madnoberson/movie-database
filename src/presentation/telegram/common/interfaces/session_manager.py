from abc import ABC, abstractmethod
from typing import Any


class SessionManager(ABC):

    @abstractmethod
    async def open_session(self, **data) -> bool:
        """
        Opens a containing `data` session associated with the current user
        and returns `True` if session has not already been opened,
        otherwise returns `False`
        """
        raise NotImplementedError
    
    @abstractmethod
    async def close_session(self) -> bool:
        """
        Closes session associated with the current user, deletes all data
        contained in the session and returns `True` if session is open,
        otherwise returns `False`
        """
        raise NotImplementedError
    
    @abstractmethod
    async def get_session_data(self, *keys) -> dict[str, Any] | None:
        """
        Returns data from session associated with `keys` if session
        is open, otherwise returns `None`
        """
        raise NotImplementedError
    
   