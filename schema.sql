CREATE TABLE recipe (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    uuid TEXT NOT NULL,
    version INTEGER NOT NULL,
    name TEXT NOT NULL,
    unique (uuid, version)
);
CREATE INDEX idx_recipe_uuid ON recipe (uuid);
CREATE UNIQUE INDEX idx_recipe_uuid_version ON recipe (uuid, version);
CREATE TABLE ingredient (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    recipe_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    name TEXT NOT NULL,
    numerator INTEGER NOT NULL,
    denominator INTEGER NOT NULL,
    measure TEXT NOT NULL
);
CREATE INDEX idx_ingredient_recipe_id ON ingredient (recipe_id);
CREATE TABLE step (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    recipe_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    name TEXT NOT NULL,
    duration_minute INTEGER NOT NULL
);
CREATE INDEX idx_step_recipe_id ON step (recipe_id);