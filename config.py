"""Configuration for the movie database project."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

MOVIES_FILE = Path('movies.json')

DB_URL = os.getenv("DB_URL", "sqlite:///movies.db")
DB_ECHO = os.getenv("DB_ECHO", "false").lower() == "true"