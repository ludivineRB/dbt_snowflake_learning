from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.item import Item, ItemCreate
from app.services import item_service

router = APIRouter()


@router.post("/", response_model=Item)
def create_item(
    *,
    db: Session = Depends(get_db),
    item_in: ItemCreate,
) -> Item:
    item = item_service.create_item(db=db, item_create=item_in)
    return item


@router.get("/", response_model=List[Item])
def read_items(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[Item]:
    items = item_service.get_items(db, skip=skip, limit=limit)
    return items


@router.get("/{item_id}", response_model=Item)
def read_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
) -> Item:
    item = item_service.get_item(db=db, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item