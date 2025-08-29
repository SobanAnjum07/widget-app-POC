from fastapi import APIRouter
from .endpoints import catalogue, checkout

api_router = APIRouter()
api_router.include_router(catalogue.router, prefix="/catalogue", tags=["catalogue"])
api_router.include_router(checkout.router, prefix="/checkout", tags=["checkout"])
