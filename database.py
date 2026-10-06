import json

from models import Movie

def load_movies(filename: str) -> dict[int, Movie]:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

            return {
                int(movie_id): movie
                for movie_id, movie in data.items()
            }

    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return {}

    except json.JSONDecodeError as e:
        print("JSON decode error: {e}")
        return{}
