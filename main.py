import db
from fastapi import FastAPI
from schema import CreateRecipe, GetRecipe
from uuid import UUID

app = FastAPI()


@app.on_event("startup")
def init_db():
    db.init()


@app.post("/recipe", response_model=GetRecipe)
def create_recipe(recipe: CreateRecipe):
    return db.create_recipe(recipe=recipe)


@app.post("/recipe/{uuid}", response_model=GetRecipe)
def create_recipe_version(uuid: UUID, recipe: CreateRecipe):
    return db.create_recipe_version(uuid=uuid, recipe=recipe)


@app.get("/recipe/{uuid}", response_model=GetRecipe)
def get_latest_recipe_version(uuid: UUID):
    return db.get_latest_recipe_version(uuid=uuid)


@app.get("/recipe/{uuid}/version/{version}", response_model=GetRecipe)
def get_recipe_version(uuid: UUID, version: int):
    return db.get_recipe_version(uuid=uuid, version=version)
