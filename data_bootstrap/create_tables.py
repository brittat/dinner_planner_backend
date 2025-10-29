from MySQLdb import connect

create_statements = {"ingredient": """CREATE TABLE `ingredient` (
  `ingredient_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `ingredient` varchar(64) DEFAULT NULL,
  `sort`          INT(10) UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`ingredient_id`),
  UNIQUE (`ingredient`)
)""",
"recipe": """CREATE TABLE `recipe` (
  `recipe_id`    INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name`         VARCHAR(128) DEFAULT NULL,
  `description`  TEXT,
  `instructions` TEXT,
  PRIMARY KEY (`recipe_id`)
)""",
"unit":"""CREATE TABLE `unit` (
  `unit_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `label`   VARCHAR(64) DEFAULT NULL,
  `sort`    INT(10) UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`unit_id`)
)""",
"recipe_ingredient":"""CREATE TABLE `recipe_ingredient` (
  `recipe_ingredient_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `recipe_id`            INT(10) UNSIGNED NOT NULL,
  `ingredient_id`        INT(10) UNSIGNED NOT NULL,
  `unit_id`              INT(10) UNSIGNED NOT NULL,
  `amount`               DECIMAL(18,9) DEFAULT NULL,
  `state`                VARCHAR(64) DEFAULT NULL,
  `sort`                 INT(10) UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`recipe_ingredient_id`),
  FOREIGN KEY (`ingredient_id`) REFERENCES `ingredient`(`ingredient_id`)
)"""}


drop_statements = """
SET FOREIGN_KEY_CHECKS = 0;
drop table if exists recipe;
drop table if exists recipe_ingredient;
drop table if exists unit;
drop table if exists ingredient;
SET FOREIGN_KEY_CHECKS = 1;
"""

cnx = connect(user='korvivar', password='bananarama',
                              host='localhost',
                              database='recipes')

cursor = cnx.cursor()

cursor.execute(drop_statements)


for create_statement in create_statements.values():
    cursor.execute(create_statement)

cnx.close()