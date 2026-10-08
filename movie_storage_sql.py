"""SQLite-backed movie storage helpers."""

from sqlalchemy import create_engine, text

import config
from models import Movie

engine = create_engine(config.DB_URL, echo=config.DB_ECHO)


def init_db() -> None:
    """Create the movies table if it does not already exist."""
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL,
                poster_url TEXT
            )
        """))
        connection.commit()


def list_movies() -> dict[int, Movie]:
    """Return all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text(
                "SELECT id, title, year, rating, poster_url FROM movies"
            )
        )
        movies = result.fetchall()

    return {
        row[0]: {
            "title": row[1],
            "year": row[2],
            "rating": row[3],
            "poster_url": row[4] or "N/A"}
            for row in movies
        }


def add_movie(title: str, year: int, rating: float, poster_url: str = "N/A") -> bool:
    """Add a movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text(
                    "INSERT INTO movies (title, year, rating, poster_url) "
                    "VALUES (:title, :year, :rating, :poster_url)"
                ),
                {
                    "title": title,
                    "year": year,
                    "rating": rating,
                    "poster_url": poster_url},
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
    """Update a movie rating in the database."""
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
