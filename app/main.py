from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from web.routes.ingredients import router as ingredients_router

app = FastAPI()

app.include_router(ingredients_router)

@app.get("/")
def root():
    return RedirectResponse("/ingredients")