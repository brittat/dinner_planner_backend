units = ['msk', 'tsk', 'krm', 'g', 'dl', 'ml', 'l', 'kg']

unit_insert_statements = [f'INSERT INTO unit(`label`) VALUES ("{unit}")' for unit in units]
