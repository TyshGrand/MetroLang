import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase

load_dotenv()

DB_URL = os.getenv('DATABASE_URL')

class DB_Connector(SQLDatabase):
    _instance = None


    def __new__(cls, db_url = DB_URL):
        if cls._instance is None:
            cls._instance = super(DB_Connector, cls).__new__(cls)
            cls._instance = SQLDatabase.from_uri(DB_URL)
        return cls._instance
    




if __name__ == "__main__":
    print(DB_URL)

    db = DB_Connector()
    print(db.run('Select * from orders limit 5'))
    