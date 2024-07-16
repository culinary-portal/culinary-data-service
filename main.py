import ConnectionToDatabase


def main():
    database = ConnectionToDatabase.ConnectionToDatabase("postgres", "postgres", "postgres", "localhost", 5432)
    database.connect()

if __name__ == "__main__":
    main()
