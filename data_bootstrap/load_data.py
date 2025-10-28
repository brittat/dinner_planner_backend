import json
import argparse
import sys
from MySQLdb import connect
import pathlib

from load_ingredients import ingredient_insert_statements
from data_bootstrap.load_units import unit_insert_statements

def load_data(cnx):
    cursor = cnx.cursor()
    for statement in ingredient_insert_statements + unit_insert_statements:
        cursor.execute(statement)
    cnx.commit()    
    cnx.close()


def argparser(command_line_arguments: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='Load dinner data',
        description='Load data into dinner planning backend')
    parser.add_argument('-e', '--env', choices=['dev', 'prod'], default='dev') 
    return parser.parse_args(command_line_arguments)

def main(command_line_arguments):
    args = argparser(command_line_arguments=command_line_arguments)
    with open(str(pathlib.Path().resolve())+"/.secrets.json", "r") as f:
        secrets = json.load(f)
        connection_params = secrets.get(args.env)

    cnx = connect(user=connection_params['user'],
                  password=connection_params['password'],
                  host=connection_params['host'],
                  database='recipes')

    load_data(cnx)
#    a = read_data(cnx)

if __name__ == "__main__":
    main(sys.argv[1:])