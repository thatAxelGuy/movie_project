import json

from models import Movie


def load_movies(filename: str) -> dict[int, Movie]:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

            return {int(movie_id): movie for movie_id, movie in data.items()}

    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return {}

    except json.JSONDecodeError:
        print("JSON decode error: {e}")
        return {}


def save_movies(filename: str, movies: dict[int, Movie]) -> None:
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(movies, file, indent=4)
    except OSError as e:
        print(f"Error saving movies: {e}")
