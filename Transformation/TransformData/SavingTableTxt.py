class SavingTable:
    def __init__(self, query, table):
        with open(f'ClearData/{table}.sql', 'a', encoding="utf-8") as file:
            file.write(query + '\n')
