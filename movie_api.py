"""OMDb API client helpers."""

import os

import requests
from dotenv import load_dotenv

from colors import error

load_dotenv()


API_KEY = os.getenv("OMDB_API_KEY")

if not API_KEY:
    raise ValueError("OMDB_API_KEY is not set in the environment.")

DATA_URL = "http://www.omdbapi.com/"
POSTER_URL = f"http://img.omdbapi.com/?apikey={API_KEY}&"


def get_movie_from_api(imdb_id: str) -> dict | None:
    """Fetch detailed movie data from the OMDb API."""
    try:
        response = requests.get(
            DATA_URL,
            params={
                "apikey": API_KEY,
                "i": imdb_id,
            },
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(error(f"Could not connect to OMDb API: {e}"))
        return None


def search_movies_from_api(title: str) -> dict | None:
    """Search for movies by title in the OMDb API."""
    try:
        response = requests.get(
            DATA_URL,
            params={
                "apikey": API_KEY,
                "s": title,
                "type": "movie",
            },
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(error(f"Could not connect to OMDb API: {e}"))
        return None
