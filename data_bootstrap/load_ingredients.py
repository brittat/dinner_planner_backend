ingredients = ["mjöl",
"kikärter",
"vaniljsocker"]

ingredient_insert_statements = [f'INSERT INTO ingredient(`ingredient`) VALUES ("{ingredient}")' for ingredient in ingredients]