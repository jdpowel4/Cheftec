import csv
import io
import logging
from fastapi import APIRouter, Depends, Form, Request, Query, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from core.database import get_db
from models.ingredient import Ingredient

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="web/templates")
logger.debug("Ingredient routes loaded.")
@router.get("/ingredients")
def ingredients_page(
    request: Request,
    db: Session = Depends(get_db)
):
    logger.debug("Fetching all ingredients for ingredients page.")
    ingredients = (
        db.query(Ingredient)
        .order_by(Ingredient.name)
        .all()
    )
    logger.debug(f"Fetched {len(ingredients)} ingredients.")
    return templates.TemplateResponse(
        "ingredients/index.html",
        {
            "request": request,
            "ingredients": ingredients
        }
    )
 
@router.get("/ingredients/search")
def ingredient_search(
    request: Request,
    q: str = "",
    vendor_item_id: int | None = None,
    db: Session = Depends(get_db)
):
    logger.debug(f"Searching ingredients with query: {q}")
    ingredients = (
        db.query(Ingredient)
        .filter(Ingredient.name.ilike(f"%{q}%"))
        .order_by(Ingredient.name)
        .all()
    )
    logger.debug(f"Found {len(ingredients)} ingredients matching query.")  
    return templates.TemplateResponse(
        "ingredients/_search_results.html",
        {
            "request": request,
            "ingredients": ingredients,
            "vendor_item_id": vendor_item_id
        }
    )

@router.get("/ingredients/search-modal")
def ingredient_search_modal(
    request: Request,
    q: str = "",
    vendor_item_id: int | None = None,
    db: Session = Depends(get_db)
):
    print("Initializing ingredient search in modal.")
    print("Query:", q)
    ingredients = (
        db.query(Ingredient)
        .filter(Ingredient.name.ilike(f"%{q}%"))
        .order_by(Ingredient.name)
        .all()
    )
    print(f"Found {len(ingredients)} ingredients matching query.")
    return templates.TemplateResponse(
        "ingredients/_picker_results.html",
        {
            "request": request,
            "ingredients": ingredients,
            "vendor_item_id": vendor_item_id
        }
    )

@router.get("/api/ingredients")
def api_ingredients(
    local_kw: str | None = Query(None),
    db: Session = Depends(get_db)
):
    return ingredient_service.search(db, local_kw)

@router.get("/ingredients/picker")
def ingredient_picker(
    request: Request,
    vendor_item_id: int
):
    print("Rendering ingredient picker modal.")
    print("Vendor Item ID:", vendor_item_id)
    return templates.TemplateResponse(
        "ingredients/picker_modal.html",
        {
            "request": request,
            "vendor_item_id": vendor_item_id
        }
    )


@router.post("/ingredients")
def create_ingredient(
    request: Request,
    name: str = Form(...),
    base_unit: str | None = Form(None),
    db: Session = Depends(get_db)
):
    logger.debug(f"Creating ingredient with name: {name}")
    logger.debug("Checking for existing ingredient.")
    exists = (
        db.query(Ingredient)
        .filter(Ingredient.name.ilike(name))
        .first()
    )
    if exists:
        logger.debug("Ingredient already exists, not creating.")
        return HTMLResponse(
            content="",
            status_code=204
        )
    ingredient = Ingredient(
        name = name.strip(),
        base_unit = base_unit
    )
    logger.debug("Adding new ingredient to database.")
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    logger.debug(f"Ingredient {ingredient.name} created with ID {ingredient.id}.")
    return templates.TemplateResponse(
        "ingredients/_rows.html",
        {
            "request": request,
            "ingredients": [ingredient]
        }
    ) 

@router.post("/ingredients/import", response_class=HTMLResponse)
def import_ingredients(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    logger.debug(f"Importing ingredients from file: {file.filename}")
    content = file.file.read().decode("utf-8-sig")
    logger.debug("File content read successfully.")
    reader = csv.DictReader(io.StringIO(content))
    created = []

    for row in reader:
        
        normalized = {k.strip().lower(): v for k, v in row.items()}
        
        name = (normalized.get("name")
            or normalized.get("ingredient"))
        
        base_unit = (normalized.get("base_unit")
            or normalized.get("unit")
            or "").strip()
       
        if not name:
            continue
        logger.debug(f"Processing ingredient: {name}")
        logger.debug("Checking for existing ingredient.")
        exists = (
            db.query(Ingredient)
            .filter(Ingredient.name.ilike(name))
            .first()
        )

        if exists:
            logger.debug("Ingredient already exists, skipping.")
            continue

        ingredient = Ingredient(
            name = name,
            base_unit = base_unit or None
        )
        logger.debug("Adding new ingredient to database session.")
        db.add(ingredient)
        logger.debug(f"Ingredient {name} added to database.")
        created.append(ingredient)
    logger.debug(f"Committing {len(created)} new ingredients to database.")
    db.commit()

    return templates.TemplateResponse(
        "ingredients/_rows.html",
        {
            "request": request,
            "ingredients": created
        }
    )