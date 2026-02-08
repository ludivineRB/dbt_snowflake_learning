from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.item import Item
from app.schemas.item import ItemCreate


def get_item(db: Session, item_id: int) -> Optional[Item]:
    return db.query(Item).filter(Item.id == item_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    return db.query(Item).offset(skip).limit(limit).all()


def create_item(db: Session, item_create: ItemCreate) -> Item:
    db_item = Item(
        title=item_create.title,
        description=item_create.description,
        owner_id=item_create.owner_id,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item