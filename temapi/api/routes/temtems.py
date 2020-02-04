from typing import Union

from fastapi import APIRouter, HTTPException

from temapi.api.loaders.temtems import temtem_loader
from temapi.api.models import ContentList, PartialTemtem, FullTemtem

router = APIRouter()


@router.get(
    '/',
    response_model=ContentList[PartialTemtem],
)
def list_temtems():
    return ContentList(
        content=temtem_loader.all(),
    )


@router.get(
    '/{id_or_name}',
    response_model=FullTemtem,
)
def get_temtem_by_id_or_name(id_or_name: Union[int, str]):
    if isinstance(id_or_name, int):
        temtem = temtem_loader.get_by_id(id_or_name)
        if temtem is None:
            raise HTTPException(404, f'Temtem with id {id_or_name} not found')

        return temtem

    temtem = temtem_loader.get_by_name(id_or_name)
    if temtem is None:
        raise HTTPException(404, f'Temtem with name {id_or_name} not found')

    return temtem
