class SavingTable:
    def __init__(self):
        pass

    def save_query_to_file(query, table):
        with open(f'Insert/inserts_{table}.sql', 'a', encoding="utf-8") as file:
            file.write(query + '\n')
