import json
import sys
import MySQLdb
import pathlib
from MySQLdb import connect


recipes = {
    "pankis":
    {
        "description":"boop",
        "instructions": "Blanda mjöl och mjlök, stek pankis",
        "ingredients":
            {
                "mjöl":
                    {
                        "unit": "dl",
                        "amount": 2
                    },
                "mjölk":
                    {
                        "unit": "dl",
                        "amount": 5
                    },
                "ägg":
                    {
                    "unit": "st",
                    "amount": 2
                    }
            }
    },
    "köttisar":
    {
        "description":"boop",
        "instructions": "blanda gojs, rulla köttbullar",
        "ingredients":
            {
                "köttfärs":
                    {
                        "unit": "gr",
                        "amount": 500
                    },
                "ströbröd":
                    {
                        "unit": "msk",
                        "amount": 2
                    },
                "ägg":
                    {
                        "unit": "st",
                        "amount": 1
                    }
            }
    }
}

ingredient_insert_statements = [f'INSERT IGNORE INTO ingredient(`ingredient`) VALUES ("{recipe}")' for recipe in recipes]

class IngredientHandler:
    def __init__(self):
        self.ingredients = self.get_all_ingredients()

    def get_all_ingredients(self):
        cnx = get_cnx()
        cursor = cnx.cursor()

        cursor.execute("DESCRIBE recipes.ingredient;")
        cols = cursor.fetchall()

        cursor.execute("SELECT * FROM recipes.ingredient;")
        ingredients = cursor.fetchall()

        return [{cols[n][0]: ingredient[n] for n in range(len(ingredient))} for ingredient in ingredients]


    def create_ingredient(self, ingredient_name):
        insert_statement = f'INSERT INTO ingredient(`ingredient`) VALUES ("{ingredient_name}")'
        cnx = get_cnx()
        cursor = cnx.cursor()
        cursor.execute(insert_statement)
        cnx.commit()
        cnx.close()

    def map_ingredient_id(self, ingredient_name:str) -> int:
        boop = [ingredient['ingredient_id'] for ingredient in self.ingredients if ingredient['ingredient']==ingredient_name]
        if not boop:
            self.create_ingredient(ingredient_name=ingredient_name)
            self.ingredients = self.get_all_ingredients()
            return self.map_ingredient_id(ingredient_name=ingredient_name)
        if len(boop) == 1:
            return boop[0]
        else:
            raise ValueError("Found multiple DB matches for ingredient %s", ingredient_name)

class UnitHandler:
    def __init__(self):
        self.units = self.get_all_units()

    def get_all_units(self):
        cnx = get_cnx()
        cursor = cnx.cursor()

        cursor.execute("DESCRIBE recipes.unit;")
        cols = cursor.fetchall()

        cursor.execute("SELECT * FROM recipes.unit;")
        units = cursor.fetchall()

        return [{cols[n][0]: unit[n] for n in range(len(unit))} for unit in units]


    def map_unit_id(self, unit_name:str) -> int:
        boop = [unit['unit_id'] for unit in self.units if unit['label']==unit_name]
        if not boop:
            raise ValueError("Found no DB matches for unit %s", unit_name)
        else:
            return boop[0]

def load_recipes():
    ingredient_handler = IngredientHandler()
    unit_handler = UnitHandler()
    cnx = get_cnx()
    cursor = cnx.cursor()
    cursor.execute('SET information_schema_stats_expiry = 0;')
    cursor.execute("SHOW TABLE STATUS LIKE 'recipe';")
    cols = cursor.fetchall()

    recipe_insert_statement_template = """INSERT IGNORE INTO recipes.recipe
                                        (recipe_id, name, description, instructions)
                                        VALUES({recipe_id}, '{name}', '{description}', '{instructions}');"""

    recipe_id = cols[0][10] if cols[0][10] else 0
    for recipe_name, recipe_details in recipes.items():
        insert_statement = recipe_insert_statement_template.format(
            recipe_id=recipe_id,
            name=recipe_name,
            description=recipe_details['description'],
            instructions=recipe_details['instructions'])

        cursor = cnx.cursor()
        try:
            cursor.execute(insert_statement)
        except Exception:
            print("This statment failed:")
            print(insert_statement)

        recipe_ingredient_insert_statement_template = """INSERT IGNORE INTO recipes.recipe_ingredient
                                        (recipe_id, ingredient_id, unit_id, amount)
                                        VALUES({recipe_id}, '{ingredient_id}', '{unit_id}', '{amount}');"""



        for ingredient, ingredient_details in recipe_details.get('ingredients').items():
            unit_id = unit_handler.map_unit_id(ingredient_details['unit'])
            ingredient_id = ingredient_handler.map_ingredient_id(ingredient)

            insert_statement = recipe_ingredient_insert_statement_template.format(
                recipe_id=recipe_id,
                ingredient_id=ingredient_id,
                unit_id=unit_id,
                amount=ingredient_details['amount'])

            try:
                cursor.execute(insert_statement)
            except Exception:
                print("This statment failed:")
                print(insert_statement)

        recipe_id = recipe_id + 1

    cnx.commit()
    cnx.close()

def get_cnx():
    with open(str(pathlib.Path().resolve())+"/.secrets.json", "r") as f:
        secrets = json.load(f)
        connection_params = secrets.get('dev')

    return connect(user=connection_params['user'],
                  password=connection_params['password'],
                  host=connection_params['host'],
                  database='recipes')

def main():
    load_recipes()

if __name__ == "__main__":
    main()
