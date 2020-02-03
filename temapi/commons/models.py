from enum import Enum
from typing import List, Optional, Dict

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


class TechniqueCategory(str, Enum):
    PHYSICAL = 'Physical'
    SPECIAL = 'Special'
    STATUS = 'Status'


class Temtem(BaseModel):
    id: int
    name: str
    image: Optional[str]
    types: List[TemtemType]

    status: Dict
    traits: List[str]
    tv_yield: str

    evolves_from: Optional[str]
    evolves_to: List[str]
    evolve_info: Optional[str]

    height: Optional[float]
    weight: Optional[float]
    cry: Optional[str]


class Technique(BaseModel):
    name: str
    description: str
    type: Optional[TemtemType]
    category: Optional[TechniqueCategory]
    damage: Optional[int]
    stamina_cost: Optional[int]
    hold: Optional[int]
    priority: Optional[int]  # 🤔
    targets: Optional[str]
    synergy: Optional[TemtemType]
    synergy_effect: Optional[str]


class Trait(BaseModel):
    name: str
    effect: str
    learned_by: List[str]


class Item(BaseModel):
    name: str
    category: str
    consumable: Optional[bool]
    limited_quantity: Optional[bool]
    purchasable: Optional[bool]
    buy_price: Optional[int]
    sell_price: Optional[int]
    description: str


class Medicine(Item):
    restore_amount: str


class ErrorItem(BaseModel):
    name: str
    error: str
