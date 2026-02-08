from typing import Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class ItemCreate(ItemBase):
    title: str
    owner_id: int


class ItemUpdate(ItemBase):
    pass


class ItemInDBBase(ItemBase):
    id: Optional[int] = None
    title: Optional[str] = None
    owner_id: Optional[int] = None

    class Config:
        from_attributes = True


class Item(ItemInDBBase):
    pass


class ItemInDB(ItemInDBBase):
    pass