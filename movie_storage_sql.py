"""
Handles SQLite storage for the movie database.
"""

from sqlalchemy import create_engine, text
from models import Movie

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=True)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL
        )
    """))
    connection.commit()


def list_movies() -> dict[int, Movie]:
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT id, title, year, rating FROM movies"))
        movies = result.fetchall()

    return {
        row[0]: {
            "title": row[1],
            "year": row[2],
            "rating": row[3]}
            for row in movies
        }


def add_movie(title: str, year: int, rating: float) -> bool:
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text(
                    "INSERT INTO movies (title, year, rating) "
                    "VALUES (:title, :year, :rating)"
                ),
                {"title": title, "year": year, "rating": rating},
            )
            connection.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False


def delete_movie(movie_id: int) -> bool:
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            result = connection.execute(
                text("DELETE FROM movies WHERE id = :id"), {"id": movie_id}
            )
            connection.commit()
            return result.rowcount > 0
        except Exception as e:
            print(f"Error: {e}")
            return False


def update_movie(movie_id: int, rating: float) -> bool:
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            result = connection.execute(
                text("UPDATE movies SET rating = :rating " "WHERE id = :id"),
                {"id": movie_id, "rating": rating},
            )
            connection.commit()
            return result.rowcount > 0
        except Exception as e:
            print(f"Error: {e}")
            return False
