"""
Handles persistent storage for the movie database.

This module is responsible for loading, saving, adding, updating,
and deleting movies in the JSON database. It does not handle user
input or display.
"""
import json

from config import MOVIES_FILE
from models import Movie


def get_movies() -> dict[int, Movie]:
    """
    Loads all movies from the JSON database.

    Returns:
        dict[int, Movie]: A dictionary containing all movies.
    """
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
    """
    Adds a movie to the JSON database.

    Args:
        title: The title of the movie.
        year: The year the movie was released.
        rating: The movie's rating.

    Returns:
        bool: True if the movie was successfully saved, otherwise False.
    """
    movies = get_movies()
    
    movie_id = max(movies, default=0) + 1
    
    movies[movie_id] = {
                    "title": title,
                    "rating": rating,
                    "year": year,
                }
    
    return save_movies(movies)


def save_movies(movies: dict[int, Movie]) -> bool:
    """
    Saves all movies to the JSON database.

    Args:
        movies: The dictionary of movies to save.

    Returns:
        bool: True if the movies were successfully saved, otherwise False.
    """
    try:
        with open(MOVIES_FILE, "w", encoding="utf-8") as file:
            json.dump(movies, file, indent=4)
            return True
    except OSError as e:
        print(f"Error saving movies: {e}")
        return False


def update_movie(movie_id: int, rating: float) -> bool:
    """
    Updates a movie's rating in the JSON database.

    Args:
        movie_id: The ID of the movie to update.
        rating: The new rating.

    Returns:
        bool: True if the movie was successfully updated and saved,
        otherwise False.
    """
    movies = get_movies()

    if movie_id not in movies:
        return False

    movies[movie_id]['rating'] = rating

    return save_movies(movies)

def delete_movie(movie_id: int) -> bool:
    """
    Deletes a movie from the JSON database.

    Args:
        movie_id: The ID of the movie to delete.

    Returns:
        bool: True if the movie was successfully deleted and saved,
        otherwise False.
    """
    movies = get_movies()

    if movie_id not in movies:
        return False

    del movies[movie_id]

    return save_movies(movies)