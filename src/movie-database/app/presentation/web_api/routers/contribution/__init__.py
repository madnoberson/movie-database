from fastapi import APIRouter

from . import routes


def create_contribution_router() -> APIRouter:
    router = APIRouter(prefix="/contribution", tags=["contribution"])

    router.add_api_route(
        path="/adding_tasks", endpoint=routes.create_adding_task,
        status_code=201, methods=["post"]
    )

    return router
