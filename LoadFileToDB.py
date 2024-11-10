import psycopg2

FILE_NAME = 'contains_data.txt'
TABLE_NAME = 'contains'
PARAMS = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'
}


def load_file_to_database(file_name, table_name):
    try:
        # Connect to the PostgreSQL database and create a cursor
        connection = psycopg2.connect(**PARAMS)
        cursor = connection.cursor()

        # Open the file and read lines
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                # Remove any newline characters from the line
                row_data = line.strip()
                print(row_data)
                # Construct the SQL query
                query = f"INSERT INTO {table_name} VALUES ({row_data});"

                try:
                    # Execute the query
                    cursor.execute(query)
                except (Exception, psycopg2.DatabaseError) as error:
                    print(f"Error while inserting row: {error}")
                    connection.rollback()  # Roll back if there's an error for this row
                else:
                    connection.commit()  # Commit each row after successful insertion

        print("All rows inserted successfully")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while connecting: {error}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Run the function
load_file_to_database(FILE_NAME, TABLE_NAME)