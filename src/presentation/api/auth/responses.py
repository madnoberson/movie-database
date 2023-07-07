from typing import Literal

from src.presentation.api.common.error_schemas import BaseErrorSchema



def get_register_responses() -> dict:
    return {
        201: {"model": Literal[True]},
        409: {"model": BaseErrorSchema}
    }


def get_login_responses() -> dict:
    return {
        200: {"model": Literal[True]},
        401: {"model": BaseErrorSchema},
        404: {"model": BaseErrorSchema}
    }
    
