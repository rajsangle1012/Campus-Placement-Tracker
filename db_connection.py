import sqlite3
import os
from dotenv import load_dotenv

# .env load krne ke liye
load_dotenv()

def get_connection():
    db_path = os.getenv("SQLITE_DB_PATH", "db/placement.db")
    
    # directory bnegi agar nhi hogi toh
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection