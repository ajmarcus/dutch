from enum import Enum
from pydantic import BaseModel, HttpUrl
from typing import List
from uuid import UUID


class Unit(str, Enum):
    cup = "cup"
    deciliter = "deciliter"
    fluid_ounce = "fluid_ounce"
    gallon = "gallon"
    gram = "gram"
    kilogram = "kilogram"
    liter = "liter"
    milligram = "milligram"
    milliliter = "milliliter"
    ounce = "ounce"
    packet = "packet"
    pint = "pint"
    pound = "pound"
    quart = "quart"
    scoop = "scoop"
    tablespoon = "tablespoon"
    teaspoon = "teaspoon"


class Ingredient(BaseModel):
    name: str
    numerator: int
    denominator: int
    unit: Unit


class Step(BaseModel):
    name: str
    duration_minute: int
    ingredients: List[Ingredient]


class CreateRecipe(BaseModel):
    name: str
    image_uuid: UUID
    steps: List[Step]


class GetRecipe(BaseModel):
    uuid: UUID
    version: int
    name: str
    duration_minute: int
    image_url: HttpUrl
    ingredients: List[Ingredient]
    steps: List[Step]