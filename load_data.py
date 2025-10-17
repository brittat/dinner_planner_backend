from MySQLdb import connect

from load_ingredients import ingredient_insert_statements
from load_units import unit_insert_statements

cnx = connect(user='korvivar', password='bananarama',
                              host='localhost',
                              database='recipes')

cursor = cnx.cursor()
for statement in ingredient_insert_statements + unit_insert_statements:
    cursor.execute(statement)
cnx.commit()    
cnx.close()