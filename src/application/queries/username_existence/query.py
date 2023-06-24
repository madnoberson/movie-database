from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CheckUsernameExistenceQuery:
    
    username: str


@dataclass(frozen=True, slots=True)
class CheckUsernameExistenceQueryResult:

    exists: bool