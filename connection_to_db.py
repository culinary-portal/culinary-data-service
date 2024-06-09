import psycopg2
from psycopg2 import OperationalError


class Database:
    def __init__(self, dbname, username, password, host, port):
        self.dbname = dbname
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(dbname=self.dbname,
                                         user= self.username,
                                         password=self.password,
                                         host=self.host,
                                         port=self.port)
            print("Connection to postgres succesfully established")
            return self.conn
        except OperationalError as error:
            print("Connection to postgres unsuccessful")
            self.conn = None
            self.cursor = None

