from typing import Union
import json
from MySQLdb import connect

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


def get_all_ingredients():
#    with open("../.secrets.json", "r") as f:
#        secrets = json.load(f)
#        connection_params = secrets.get('dev')

    cnx = connect(user="korvivar",
                  password="bananarama",
                  host="localhost",
                  database='recipes')

    cursor = cnx.cursor()

    cursor.execute("DESCRIBE recipes.ingredient;")
    cols = cursor.fetchall()

    cursor.execute("SELECT * FROM recipes.ingredient;")
    ingredients = cursor.fetchall()

    return [{cols[n][0]: ingredient[n] for n in range(len(ingredient))} for ingredient in ingredients]

