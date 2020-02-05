from fastapi import APIRouter, HTTPException

from temapi.api.loaders.techniques import technique_loader
from temapi.commons.models import Technique

router = APIRouter()


@router.get(
    '/{name}', response_model=Technique,
)
def get_technique(name: str):
    technique = technique_loader.get_by_name(name)
    if technique is None:
        raise HTTPException(404, f'Technique named {name} not found')

    return technique
