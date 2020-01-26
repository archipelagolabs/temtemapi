from typing import List, Union

from fastapi import APIRouter, HTTPException

from temapi.api.loaders import TemtemLoader
from temapi.commons.models import Temtem

router = APIRouter()

temtem_loader = TemtemLoader()


@router.get(
    '/',
    response_model=List[Temtem],
)
def list_temtems():
    return temtem_loader.temtems


@router.get(
    '/{id_or_name}',
    response_model=Temtem,
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
