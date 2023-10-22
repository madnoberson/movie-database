from fastapi import APIRouter

from . import routes


def create_contribution_router() -> APIRouter:
    router = APIRouter(prefix="/contribution", tags=["contribution"])

    router.include_router(_create_adding_tasks_router())

    return router


def _create_adding_tasks_router() -> APIRouter:
    router = APIRouter(prefix="/adding_tasks", tags=["adding_tasks"])

    router.add_api_route(
        path="/", endpoint=routes.create_adding_task,
        status_code=201, methods=["post"]
    )

    return router