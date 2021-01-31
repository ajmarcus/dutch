from schema import CreateRecipe, GetRecipe
from uuid import UUID

DEFAULT_UUID = UUID("96ea218c-b71b-4142-9cb5-bc8ca35200b7")
DEFAULT_RECIPE = GetRecipe(
    uuid=DEFAULT_UUID,
    version=0,
    name="default",
    duration_minute=0,
    image_url=f"https://www.forkfork.dev/image/{DEFAULT_UUID}",
    ingredients=[],
    steps=[],
)


def create_image() -> UUID:
    return DEFAULT_UUID


def create_recipe(recipe: CreateRecipe) -> GetRecipe:
    return DEFAULT_RECIPE


def create_recipe_version(uuid: UUID, recipe: CreateRecipe) -> GetRecipe:
    return DEFAULT_RECIPE


def get_latest_recipe_version(uuid: UUID) -> GetRecipe:
    return DEFAULT_RECIPE


def get_recipe_version(uuid: UUID, version: int) -> GetRecipe:
    return DEFAULT_RECIPE