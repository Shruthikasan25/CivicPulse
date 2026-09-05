import os
from dotenv import load_dotenv
from sqlalchemy import create_engine,text

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env")

engine=create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        result=connection.execute(text("SELECT current_database();"))
        print("Connected to:",result.scalar())
except Exception as e:
    print("Database connection failed:")
    print(e)