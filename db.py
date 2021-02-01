import logging
import os
from sqlite3.dbapi2 import Connection
from schema import CreateRecipe, GetRecipe, Ingredient, Measure, Step
from sqlite3 import connect
from uuid import UUID, uuid4


CWD = os.getcwd()
DB_FILE = CWD + "/dutch.db"
DEFAULT_UUID = UUID("0edbf298-4e43-40c1-b438-74e3ba7aa2f3")
DEFAULT_RECIPE = GetRecipe(
    uuid=DEFAULT_UUID,
    version=0,
    name="default",
    duration_minute=0,
    ingredients=[],
    steps=[],
)
GET_INGREDIENTS = """SELECT name, numerator, denominator, measure
FROM ingredient
WHERE recipe_id = ?
ORDER by position ASC"""
GET_LAST_RECIPE_VERSION = """SELECT version
FROM recipe
WHERE uuid = ?
ORDER BY version DESC
LIMIT 1"""
GET_RECIPE = """SELECT r.id, r.uuid, r.version, r.name,
sum(s.duration_minute) duration_minute
FROM recipe r
JOIN step s
ON r.id = s.recipe_id
WHERE r.uuid = ? AND r.version = ?
GROUP BY 1,2,3"""
GET_STEPS = """SELECT name, duration_minute
FROM step
WHERE recipe_id = ?
ORDER BY position ASC"""
INSERT_INGREDIENT = """INSERT INTO ingredient
(recipe_id, position, name, numerator, denominator, measure)
VALUES (?,?,?,?,?,?)"""
INSERT_RECIPE = """INSERT INTO recipe
(uuid, version, name)
VALUES (?,?,?)"""
INSERT_STEP = """INSERT INTO step
(recipe_id, position, name, duration_minute)
VALUES (?,?,?,?)"""


def _get_recipe(db: Connection, uuid: UUID, version: int) -> GetRecipe:
    recipe = db.execute(GET_RECIPE, (str(uuid), version)).fetchone()
    ingredients = db.execute(GET_INGREDIENTS, (str(recipe[0])))
    steps = db.execute(GET_STEPS, (str(recipe[0])))
    return GetRecipe(
        uuid=UUID(recipe[1]),
        version=recipe[2],
        name=recipe[3],
        duration_minute=recipe[4],
        ingredients=[
            Ingredient(
                name=i[0],
                numerator=i[1],
                denominator=i[2],
                measure=Measure[i[3]],
            )
            for i in ingredients
        ],
        steps=[Step(name=s[0], duration_minute=s[1]) for s in steps],
    )


def init() -> bool:
    if os.path.isfile(DB_FILE):
        logging.info("database exists")
        os.remove(DB_FILE)
    with connect(DB_FILE) as db, open(CWD + "/schema.sql") as ddl:
        db.executescript(ddl.read())
    return True


def create_recipe(recipe: CreateRecipe) -> GetRecipe:
    with connect(DB_FILE) as db:
        uuid = uuid4()
        version = 0
        recipe_id = db.execute(
            INSERT_RECIPE, (str(uuid), version, recipe.name)
        ).lastrowid
        db.executemany(
            INSERT_INGREDIENT,
            [
                (recipe_id, position, i.name, i.numerator, i.denominator, i.measure)
                for position, i in enumerate(recipe.ingredients)
            ],
        )
        db.executemany(
            INSERT_STEP,
            [
                (recipe_id, position, s.name, s.duration_minute)
                for position, s in enumerate(recipe.steps)
            ],
        )
        return _get_recipe(db=db, uuid=uuid, version=version)


def create_recipe_version(uuid: UUID, recipe: CreateRecipe) -> GetRecipe:
    with connect(DB_FILE) as db:
        version = (
            int(db.execute(GET_LAST_RECIPE_VERSION, (str(uuid),)).fetchone()[0]) + 1
        )
        recipe_id = db.execute(
            INSERT_RECIPE, (str(uuid), version, recipe.name)
        ).lastrowid
        db.executemany(
            INSERT_INGREDIENT,
            [
                (recipe_id, position, i.name, i.numerator, i.denominator, i.measure)
                for position, i in enumerate(recipe.ingredients)
            ],
        )
        db.executemany(
            INSERT_STEP,
            [
                (recipe_id, position, s.name, s.duration_minute)
                for position, s in enumerate(recipe.steps)
            ],
        )
        return _get_recipe(db=db, uuid=uuid, version=version)


def get_latest_recipe_version(uuid: UUID) -> GetRecipe:
    with connect(DB_FILE) as db:
        version = int(db.execute(GET_LAST_RECIPE_VERSION, (str(uuid),)).fetchone()[0])
        return _get_recipe(db=db, uuid=uuid, version=version)


def get_recipe_version(uuid: UUID, version: int) -> GetRecipe:
    with connect(DB_FILE) as db:
        return _get_recipe(db=db, uuid=uuid, version=version)