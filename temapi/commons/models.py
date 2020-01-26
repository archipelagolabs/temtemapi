from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class TemtemType(str, Enum):
    NEUTRAL = 'Neutral'
    FIRE = 'Fire'
    NATURE = 'Nature'
    WATER = 'Water'
    ELECTRIC = 'Electric'
    MENTAL = 'Mental'
    EARTH = 'Earth'
    WIND = 'Wind'
    CRYSTAL = 'Crystal'
    DIGITAL = 'Digital'
    MELEE = 'Melee'
    TOXIC = 'Toxic'


class TechniqueCategory(Enum):
    PHYSICAL = 'Physical'
    SPECIAL = 'Special'
    STATUS = 'Status'


class Temtem(BaseModel):
    id: int
    name: str
    types: List[TemtemType]
    evolves_from: Optional[str]
    evolves_to: List[str]
    traits: List[str]
    tv_yield: str
    height: Optional[float]
    weight: Optional[float]
    cry: Optional[str]


class Technique(BaseModel):
    name: str
    description: str
    type: TemtemType
    category: TechniqueCategory
    damage: int
    stamina_cost: int
    hold: int
    priority: int  # 🤔
    targets: str
    synergy: Optional[str]  # TemtemType
    synergy_effect: Optional[str]


class Item(BaseModel):
    name: str
    effect: str
    consumable: bool


class Trait(BaseModel):
    name: str
    effect: str
    learned_by: List[str]
