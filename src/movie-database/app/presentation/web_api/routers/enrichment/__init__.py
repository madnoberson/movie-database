from fastapi import APIRouter

from . import routes


def create_enrichment_router() -> APIRouter:
    router = APIRouter(prefix="/enrichment", tags=["enrichment"])

    router.include_router(_create_enrichment_tasks_router())

    return router


def _create_enrichment_tasks_router() -> APIRouter:
    router = APIRouter(prefix="/tasks", tags=["enrichment_tasks"])

    router.add_api_route(
        path="/", endpoint=routes.create_enrichment_task,
        status_code=201, methods=["post"]
    )

    return router