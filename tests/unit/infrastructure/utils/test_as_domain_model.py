from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4
from enum import IntEnum

from src.infrastructure.application.utils import as_domain_model


class IntEnumExample(IntEnum):

    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3


@dataclass(slots=True)
class DomainModelExample:

    uuid: UUID
    timestamp: datetime
    int_enum: IntEnumExample
    list_of_int_enums: list[IntEnumExample]


def test_func_should_return_domain_model_instance():
    expected_domain_model = DomainModelExample(
        uuid=uuid4(), timestamp=datetime.utcnow(), int_enum=IntEnumExample.VALUE_1,
        list_of_int_enums=[IntEnumExample.VALUE_2, IntEnumExample.VALUE_3]
    )
    mapping = {
        "uuid": str(expected_domain_model.uuid), "timestamp": expected_domain_model.timestamp.isoformat(),
        "int_enum": expected_domain_model.int_enum.value,
        "list_of_int_enums": [int_enum.value for int_enum in expected_domain_model.list_of_int_enums]
    }     

    assert as_domain_model(DomainModelExample, mapping) == expected_domain_model


