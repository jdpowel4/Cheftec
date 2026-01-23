import logging
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from web.routes.ingredients import router as ingredients_router
from web.routes.vendor_items import router as vendor_items_router

logger = logging.getLogger(__name__)

app = FastAPI()
logger.info("Starting application and including routers.")
app.include_router(ingredients_router)
app.include_router(vendor_items_router)

@app.get("/")
def root():
    logger.info("Redirecting to /ingredients")
    return RedirectResponse("/ingredients")