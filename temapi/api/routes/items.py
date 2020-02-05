from typing import List

from fastapi import APIRouter, HTTPException

from temapi.api.loaders.items import ItemLoader
from temapi.commons.models import Item

router = APIRouter()

item_loader = ItemLoader()


@router.get(
    '/', response_model=List[Item],
)
def list_items():
    return item_loader.items


@router.get(
    '/{name}', response_model=Item,
)
def get_item_by_name(name: str):
    item = item_loader.get_by_name(name)

    if item is None:
        raise HTTPException(404, f'Item with name {name} not found')

    return item
