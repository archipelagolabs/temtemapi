from typing import List

from fastapi import APIRouter

from temapi.api.loaders.traits import TraitLoader
from temapi.commons.models import Trait

router = APIRouter()

trait_loader = TraitLoader()


@router.get(
    '/',
    response_model=List[Trait],
)
def list_traits():
    return trait_loader.traits
