from fastapi import APIRouter, HTTPException
from temapi.api.loaders import TemtemLoader

router = APIRouter()

temtem_loader = TemtemLoader()


@router.get('/')
def list_temtems():
    return temtem_loader.temtems


@router.get('/{tid}')
def get_temtem_by_id(tid: int):
    temtem = temtem_loader.get_by_id(tid)

    if temtem is None:
        raise HTTPException(404, f'Temtem with id {tid} not found')

    return temtem
