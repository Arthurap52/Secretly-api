#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.sessions import engine
from app.db.base import Base
from app.core.config import settings
# Importa os modelos para registrar metadados no Base
from app.models import group, participant, draw  # noqa: F401

def init_db():
    print("Initializing SQLite3 database...")
    print(f"Database: {settings.database_url}")
    print("Creating tables: groups, participants, draws")
    
    try:
        db_path = settings.database_url.replace("sqlite:///", "")
        if "/" in db_path:
            db_dir = os.path.dirname(db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
                print(f"Directory created: {db_dir}")
        
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
        print("Ready-to-use database!")
    except Exception as e:
        print(f"Error creating tables.: {e}")
        print("Check if:")
        print(" - The database URL is correct in the .env file.")
        print(" - You have permission to create files in the directory.")

if __name__ == "__main__":
    init_db()

