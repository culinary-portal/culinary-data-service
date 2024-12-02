import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
FILE_NAME = 'Transformation/ClearData/ingredient_table'
TABLE_NAME = 'testing'
PARAMS = {
            'dbname': os.getenv('GCP_DB_NAME'),
            'user': os.getenv('GCP_DB_USER'),
            'password': os.getenv('GCP_DB_PASSWORD'),
            'host': os.getenv('GCP_DB_HOST'),
            'port': os.getenv('GCP_DB_PORT')
        }


def load_file_to_database(file_name, table_name):
    try:
        # connect to the PostgreSQL database and create a cursor
        connection = psycopg2.connect(**PARAMS)
        cursor = connection.cursor()
        # open the file and read lines
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                row_data = line.strip()
                print(row_data)
                # construct the SQL query
                query = f"INSERT INTO {table_name} VALUES ({row_data});"

                try:
                    # execute the query
                    cursor.execute(query)
                except (Exception, psycopg2.DatabaseError) as error:
                    print(f"Error while inserting row: {error}")
                    connection.rollback()  # roll back if there's an error for this row
                else:
                    connection.commit()  # commit each row after successful insertion

        print("All rows inserted successfully")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while connecting: {error}")

    finally:
        # close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# run the function
load_file_to_database(FILE_NAME, TABLE_NAME)