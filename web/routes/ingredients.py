from fastapi import APIRouter, Depends, Form, Request, Query
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from core.database import get_db
from models.ingredient import Ingredient

router = APIRouter()
templates = Jinja2Templates(directory="web/templates")

@router.get("/ingredients", response_class=HTMLResponse)
def ingredients_page(
    request: Request,
    db: Session = Depends(get_db)
):
    ingredients = (
        db.query(Ingredient)
        .order_by(Ingredient.name)
        .limit(50)
        .all()
    )
    return templates.TemplateResponse(
        "ingredients/index.html",
        {
            "request": request,
            "ingredients": ingredients
        }
    )

@router.get("/ingredients/search")
def search_ingredients(
    q: str = "",
    db: Session = Depends(get_db)
):
    ingredients = (
        db.query(Ingredient)
        .filter(Ingredient.name.ilike(f"%{q}%"))
        .order_by(Ingredient.name)
        .all()
    )

    return templates.TemplateResponse(
        "ingredients/_row.html",
        {
            "request": {},
            "ingreditents": ingredients
        }
    )


@router.get("/api/ingredients")
def api_ingredients(
    local_kw: str | None = Query(None),
    db: Session = Depends(get_db)
):
    return ingredient_service.search(db, local_kw)

@router.post("/ingredients")
def create_ingredient(
    name: str = Form(...),
    base_unit: str | None = Form(None),
    db: Session = Depends(get_db)
):
    print("CREATE INGREDIENT CALLED", name, base_unit)
    ingredient = Ingredient(
        name = name.strip(),
        base_unit = base_unit
    )
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)

    return templates.TemplateResponse(
        "ingredients/_rows.html",
        {
            "request": {},
            "ingredients": [ingredient]
        }
    )