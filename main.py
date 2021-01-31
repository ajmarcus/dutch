import db
from fastapi import FastAPI
from schema import CreateRecipe, GetRecipe
from uuid import UUID

app = FastAPI()


@app.post("/image", response_model=UUID)
def create_image():
    return db.DEFAULT_UUID


@app.post("/recipe", response_model=GetRecipe)
def create_recipe(recipe: CreateRecipe):
    return db.DEFAULT_RECIPE


@app.post("/recipe/{uuid}", response_model=GetRecipe)
def create_recipe_version(uuid: UUID, recipe: CreateRecipe):
    return db.DEFAULT_RECIPE


@app.get("/recipe/{uuid}", response_model=GetRecipe)
def get_latest_recipe_version(uuid: UUID):
    return db.DEFAULT_RECIPE


@app.get("/recipe/{uuid}/version/{version}", response_model=GetRecipe)
def get_recipe_version(uuid: UUID, version: int):
    return db.DEFAULT_RECIPE
