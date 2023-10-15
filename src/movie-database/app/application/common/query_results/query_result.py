from typing import TypeVar


class QueryResult:
    ...


QueryResultT = TypeVar("QueryResultT", bound=QueryResult)
