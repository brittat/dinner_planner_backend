ingredients = ["mjöl",
"kikärter",
"vaniljsocker",
"kanel"]

ingredient_insert_statements = [f'INSERT INTO ingredient(`ingredient`) VALUES ("{ingredient}")' for ingredient in ingredients]