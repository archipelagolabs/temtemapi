from fastapi import APIRouter

from temapi.api.loaders.traits import trait_loader
from temapi.api.models import ContentList
from temapi.commons.models import Trait

router = APIRouter()


@router.get(
    '/',
    response_model=ContentList[Trait],
)
def list_traits():
    return ContentList(
        content=trait_loader.traits,
    )
