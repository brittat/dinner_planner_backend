from typing import Union
import json
import pathlib
from MySQLdb import connect
from random import randint

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/ingredients")
async def read_ingredients():
    return get_all_ingredients()

def get_cnx():
    with open(str(pathlib.Path(__file__).parents[1])+"/.secrets.json", "r") as f:
        secrets = json.load(f)
        connection_params = secrets.get('dev')

    return connect(user=connection_params['user'],
                  password=connection_params['password'],
                  host=connection_params['host'],
                  database='recipes')

@app.get("/recipe_ingredients/{recipe_id}")
async def get_recipe_ingredients(recipe_id: int):
    return get_ingredients_by_recipe_id(recipe_id=recipe_id)

def get_ingredients_by_recipe_id(recipe_id: int):
    cnx = get_cnx()
    cursor = cnx.cursor()

    cursor.execute(f"""SELECT * from recipes.recipe_ingredient
                   LEFT JOIN ingredient ON recipe_ingredient.ingredient_id  = ingredient.ingredient_id
                   LEFT JOIN unit ON recipe_ingredient.unit_id = unit.unit_id WHERE recipe_id = '{recipe_id}';""")
    ingredients = cursor.fetchall()
    col_names =  [col[0] for col in cursor.description]
    ingredient_list = []
    for ingredient in ingredients:
        ingredient_list.append(dict(zip(col_names, ingredient)))

    return ingredient_list

def get_recipe(recipe_id: int):
    cnx = get_cnx()
    cursor = cnx.cursor()

    cursor.execute(f"SELECT * from recipes.recipe WHERE recipe_id='{recipe_id}';")
    recipe = cursor.fetchall()

    ingredients = get_ingredients_by_recipe_id(recipe_id=recipe_id)
    slim_ingredients = [{ingredient['ingredient']:f"{ingredient['amount']} {ingredient['label']}"} for ingredient in ingredients]
    return {**{cursor.description[n][0]: recipe[0][n] for n in range(len(recipe[0]))}, **{"ingredients": slim_ingredients}}

def get_random_recipe():
    cnx = get_cnx()
    cursor = cnx.cursor()

    cursor.execute('SET information_schema_stats_expiry = 0;')
    cursor.execute("SHOW TABLE STATUS LIKE 'recipe';")
    cols = cursor.fetchall()
    max_recipe_id = cols[0][10] if cols[0][10] else 0
    random_recipe_id = randint(0, max_recipe_id - 1)
    return get_recipe(random_recipe_id)

@app.get("/recipes/{recipe_id}")
async def get_recipe_by_id(recipe_id: int):
    return get_recipe(recipe_id=recipe_id)

def get_all_ingredients():
    cnx = get_cnx()
    cursor = cnx.cursor()

    cursor.execute("DESCRIBE recipes.ingredient;")
    cols = cursor.fetchall()

    cursor.execute("SELECT * FROM recipes.ingredient;")
    ingredients = cursor.fetchall()

    cnx.close()

    return [{cols[n][0]: ingredient[n] for n in range(len(ingredient))} for ingredient in ingredients]

