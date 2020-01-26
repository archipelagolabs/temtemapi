from enum import Enum
from typing import NamedTuple, List


class Temtem(NamedTuple):
    id: int
    name: str
    types: List[str]  # TemtemType
    evolves_from: str
    evolves_to: List[str]
    traits: List[str]
    tv_yield: str
    height: int
    weight: int
    cry: str


class Move(NamedTuple):
    id: int
    name: str
    description: str
    type: str  # TemtemType
    category: str  # MoveCategory
    power: int
    stamina: int


class Item(NamedTuple):
    id: int
    name: str
    effect: str
    consumable: bool


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


class MoveCategory(Enum):
    PHYSICAL = 'Physical'
    SPECIAL = 'Special'
    STATUS = 'Status'
