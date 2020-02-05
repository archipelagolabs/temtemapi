from typing import Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

from temapi.commons.models import TemtemType, Trait

T = TypeVar('T')


class ContentList(GenericModel, Generic[T]):
    content: List[T]


class PartialTemtem(BaseModel):
    id: int
    name: str
    types: List[TemtemType]
    image: str


class FullTemtem(PartialTemtem):
    evolves_from: Optional[str]
    evolves_to: List[str]
    evolve_info: Optional[str]

    traits: List[Trait]
    tv_yield: str
    status: Dict

    height: Optional[float]
    weight: Optional[float]
    cry: Optional[str]
