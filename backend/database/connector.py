import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase

load_dotenv()

DB_URL = os.getenv('DATABASE_URL')

def connector():
    return SQLDatabase.from_uri(DB_URL)


if __name__ == "__main__":
    print(DB_URL)

    db = connector()
    print(db.run('Select * from orders limit 5'))