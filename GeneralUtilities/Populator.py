import psycopg2


def save_query_to_file(query, table):
    with open(f'Insert/inserts_{table}.sql', 'a', encoding="utf-8") as file:
        file.write(query + '\n')


class Populator:
    def __init__(self):
        self.params = {
            'dbname': 'postgres',
            'user': 'postgres',
            'password': 'postgres',
            'host': 'localhost',
            'port': '5432'}

    def insert_row(self, table_name, row):
        try:
            # connect to the PostgreSQL database and create cursor
            connection = psycopg2.connect(**self.params)
            cursor = connection.cursor()
            try:
                query = f"""INSERT INTO {table_name} VALUES ({row});"""
                cursor.execute(query)
                connection.commit()

                print("Row inserted successfully")
                # to save the query to a seperate file
                save_query_to_file(query, table_name)
            except (Exception, psycopg2.DatabaseError) as error:
                print(f"Error while inserting: {error}")
                if connection:
                    connection.rollback()
            finally:
                # close the cursor and connection
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error while connection: {error}")
