from fastapi import APIRouter

from powerplant_challenge.api.api_v1.endpoints import productionplan

api_router = APIRouter()
api_router.include_router(productionplan.router, prefix="/productionplan", tags=["productionplan"])
