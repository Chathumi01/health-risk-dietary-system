import os
import sqlite3

# Absolute path of backend folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Absolute path to database folder
DB_DIR = os.path.join(BASE_DIR, "..", "database")

# Create database folder if it does not exist
os.makedirs(DB_DIR, exist_ok=True)

# Absolute path to database file
DB_PATH = os.path.join(DB_DIR, "health_data.db")

# Connect to SQLite database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS health_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    age INTEGER,
    gender INTEGER,
    height REAL,
    weight REAL,
    bmi REAL,
    meals_per_day INTEGER,
    activity_level INTEGER,
    risk_level INTEGER
)
""")

conn.commit()
conn.close()

print("✅ Database initialized successfully at:", DB_PATH)