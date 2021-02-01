from enum import Enum
from pydantic import BaseModel
from typing import List
from uuid import UUID


class Measure(str, Enum):
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
    measure: Measure


class Step(BaseModel):
    name: str
    duration_minute: int


class CreateRecipe(BaseModel):
    name: str
    ingredients: List[Ingredient]
    steps: List[Step]


class GetRecipe(BaseModel):
    uuid: UUID
    version: int
    name: str
    duration_minute: int
    ingredients: List[Ingredient]
    steps: List[Step]