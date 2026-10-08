"""JSON-backed movie storage helpers."""
import json

from config import MOVIES_FILE
from models import Movie


def get_movies() -> dict[int, Movie]:
    """Return all movies from the JSON database."""
    try:
        with open(MOVIES_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            return {
                int(movie_id): movie
                for movie_id, movie in data.items()
            }

    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return {}

    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return {}


def add_movie(title: str, year: int, rating: float) -> bool:
    """Add a movie to the JSON database."""
    movies = get_movies()
    
    movie_id = max(movies, default=0) + 1
    
    movies[movie_id] = {
                    "title": title,
                    "rating": rating,
                    "year": year,
                }
    
    return save_movies(movies)


def save_movies(movies: dict[int, Movie]) -> bool:
    """Write the movie dictionary to the JSON database."""
    try:
        with open(MOVIES_FILE, "w", encoding="utf-8") as file:
            json.dump(movies, file, indent=4)
            return True
    except OSError as e:
        print(f"Error saving movies: {e}")
        return False


def update_movie(movie_id: int, rating: float) -> bool:
    """Update a movie rating in the JSON database."""
    movies = get_movies()

    if movie_id not in movies:
        return False

    movies[movie_id]['rating'] = rating

    return save_movies(movies)

def delete_movie(movie_id: int) -> bool:
    """Delete a movie from the JSON database."""
    movies = get_movies()

    if movie_id not in movies:
        return False

    del movies[movie_id]

    return save_movies(movies)