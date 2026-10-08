"""Configuration for the movie database project."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path('data')
MOVIES_FILE = DATA_DIR / 'movies.json'
DB_FILE = DATA_DIR / 'movies.db'

STATIC_DIR = Path('_static')
TEMPLATE_FILE = STATIC_DIR / 'index_template.html'
OUTPUT_HTML_FILE = STATIC_DIR / 'index.html'

DB_URL = os.getenv("DB_URL", f"sqlite:///{DB_FILE.as_posix()}")
DB_ECHO = os.getenv("DB_ECHO", "false").lower() == "true"