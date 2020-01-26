from enum import Enum
from typing import NamedTuple, List, Optional


class Temtem(NamedTuple):
    id: int
    name: str
    types: List[str]  # TemtemType
    evolves_from: str
    evolves_to: List[str]
    traits: List[str]
    tv_yield: str
    height: float
    weight: float
    cry: str


class Technique(NamedTuple):
    name: str
    description: str
    type: str  # TemtemType
    category: str  # MoveCategory
    damage: int
    stamina_cost: int
    hold: int
    priority: int  # 🤔
    synergy: Optional[str]  # TemtemType


class Item(NamedTuple):
    name: str
    effect: str
    consumable: bool


class Trait(NamedTuple):
    name: str
    effect: str
    learned_by: List[str]


class TemtemType(Enum):
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
