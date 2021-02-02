#!/usr/bin/env python
import db
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from os import environ
from schema import CreateRecipe, GetRecipe
from uuid import UUID
import uvicorn

app = FastAPI()


@app.on_event("startup")
def init_db():
    db.init()


@app.get("/")
async def redirect_docs():
    return RedirectResponse("/docs")


@app.post("/recipe", response_model=GetRecipe)
async def create_recipe(recipe: CreateRecipe):
    response = db.create_recipe(recipe=recipe)
    return response


@app.post("/recipe/{uuid}", response_model=GetRecipe)
async def create_recipe_version(uuid: UUID, recipe: CreateRecipe):
    response = db.create_recipe_version(uuid=uuid, recipe=recipe)
    return response


@app.get("/recipe/{uuid}", response_model=GetRecipe)
async def get_latest_recipe_version(uuid: UUID):
    response = db.get_latest_recipe_version(uuid=uuid)
    if response is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return response


@app.get("/recipe/{uuid}/version/{version}", response_model=GetRecipe)
async def get_recipe_version(uuid: UUID, version: int):
    response = db.get_recipe_version(uuid=uuid, version=version)
    if response is None:
        raise HTTPException(status_code=404, detail="Recipe Version not found")
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(environ.get("PORT", 8080)))
