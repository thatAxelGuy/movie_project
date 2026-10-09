"""SQLite-backed movie storage helpers.

Schema (many-to-many between users and movies):
    users        one row per user
    movies       one row per film, shared by every user who added it
    user_movies  join table: which user has which movie, plus that user's note
"""

from sqlalchemy import create_engine, event, text
from sqlalchemy.exc import IntegrityError

import config
import uuid
from models import MovieWithNote

engine = create_engine(config.DB_URL, echo=config.DB_ECHO)


@event.listens_for(engine, "connect")
def _enable_foreign_keys(dbapi_connection, connection_record):
    """SQLite only enforces FOREIGN KEYs when this pragma is on, per connection."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.close()


def init_db() -> None:
    """Create the users, movies and user_movies tables if they do not exist."""
    with engine.begin() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            )
        """))

        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL,
                poster_url TEXT,
                country TEXT,

                UNIQUE(title, year)
            )
        """))

        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS user_movies (
                user_id TEXT NOT NULL,
                movie_id INTEGER NOT NULL,
                note TEXT,

                PRIMARY KEY (user_id, movie_id),
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY(movie_id) REFERENCES movies(id) ON DELETE CASCADE
            )
        """))


def create_user(name: str) -> str | None:
    """Create UUID and store user in the db.

    Returns the new user's id, or None if a user with this name already exists.
    """
    user_id = str(uuid.uuid4())

    try:
        with engine.begin() as connection:
            connection.execute(
                text("""
                    INSERT INTO users (id, name)
                    VALUES (:id, :name)
                """),
                {"id": user_id, "name": name}
            )
    except IntegrityError:
        # users.name is UNIQUE, so a duplicate name is rejected by the database.
        return None

    return user_id


def list_user_movies(user_id: str) -> dict[int, MovieWithNote]:
    """Return the given user's own movies, each with their note on it."""
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT m.id, m.title, m.year, m.rating, m.poster_url, m.country,
                       um.note
                FROM movies m
                JOIN user_movies um ON um.movie_id = m.id
                WHERE um.user_id = :user_id
                ORDER BY m.id
            """),
            {"user_id": user_id},
        )
        movies = result.fetchall()

    return {
        row[0]: {
            "title": row[1],
            "year": row[2],
            "rating": row[3],
            "poster_url": row[4] or "N/A",
            "country": row[5] or "N/A",
            "note": row[6] or "N/A",
        }
        for row in movies
    }


def get_user_by_name(name: str) -> str | None:
    """Return the id of the existing user with this name, if any."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT id FROM users WHERE name = :name"),
            {"name": name},
        )
        row = result.first()
        return row[0] if row else None


def list_users() -> list[tuple[str, str]]:
    """Return all users as (id, name) tuples, ordered by name."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT id, name FROM users ORDER BY name")
        )
        return [(row[0], row[1]) for row in result.fetchall()]


def movie_exists(user_id: str, title: str) -> bool:
    """Check whether the given user already has a movie with this title."""
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT 1
                FROM movies m
                JOIN user_movies um ON um.movie_id = m.id
                WHERE um.user_id = :user_id AND m.title = :title
            """),
            {"user_id": user_id, "title": title},
        )
        return result.first() is not None


def add_movie(
    user_id: str, title: str, year: int, rating: float, poster_url: str = "N/A"
) -> bool:
    """Add a movie to the given user's own list.

    The film itself is stored only once in `movies`; if another user already
    added it, that row is reused. Returns False if this user already has it.
    """
    # engine.begin() wraps everything in one transaction: either all of it is
    # saved, or (on an error) none of it is.
    with engine.begin() as connection:
        row = connection.execute(
            text("SELECT id FROM movies WHERE title = :title AND year = :year"),
            {"title": title, "year": year},
        ).first()

        if row:
            movie_id = row[0]
        else:
            result = connection.execute(
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
            movie_id = result.lastrowid

        already_linked = connection.execute(
            text("""
                SELECT 1 FROM user_movies
                WHERE user_id = :user_id AND movie_id = :movie_id
            """),
            {"user_id": user_id, "movie_id": movie_id},
        ).first()

        if already_linked:
            return False

        connection.execute(
            text("""
                INSERT INTO user_movies (user_id, movie_id)
                VALUES (:user_id, :movie_id)
            """),
            {"user_id": user_id, "movie_id": movie_id},
        )
        return True


def delete_movie(user_id: str, movie_id: int) -> bool:
    """Delete a movie from the given user's own list.

    If no other user still has the movie afterwards, the film itself is
    removed from `movies` too, so no orphaned rows are left behind.
    """
    with engine.begin() as connection:
        result = connection.execute(
            text("""
                DELETE FROM user_movies
                WHERE user_id = :user_id AND movie_id = :movie_id
            """),
            {"user_id": user_id, "movie_id": movie_id},
        )

        if result.rowcount == 0:
            return False

        connection.execute(
            text("""
                DELETE FROM movies
                WHERE id = :movie_id
                  AND NOT EXISTS (
                      SELECT 1 FROM user_movies WHERE movie_id = :movie_id
                  )
            """),
            {"movie_id": movie_id},
        )
        return True


def update_movie(user_id: str, movie_id: int, note: str) -> bool:
    """Set the given user's note on one of their own movies."""
    with engine.begin() as connection:
        result = connection.execute(
            text("""
                UPDATE user_movies SET note = :note
                WHERE user_id = :user_id AND movie_id = :movie_id
            """),
            {"user_id": user_id, "movie_id": movie_id, "note": note},
        )
        return result.rowcount > 0
