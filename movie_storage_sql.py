"""
Handles SQLite storage for the movie database.
"""
from sqlalchemy import create_engine, text, update

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

def list_movies() -> dict[str, dict[str, int | float]]:
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating FROM movies"))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2]} for row in movies}

def add_movie(title: str, year: int, rating: float) -> None:
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating) VALUES (:title, :year, :rating)"), 
                               {"title": title, "year": year, "rating": rating})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")

def delete_movie(title) -> bool:
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("DELETE FROM movies WHERE title = :title"),
                {"title": title}
            )
            connection.commit()
            print(f"Movie '{title}' deleted successfully.")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

def update_movie(title: str, rating: float) -> bool:
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text(
                    "UPDATE movies SET rating = :rating "
                    "WHERE title = :title"
                ),
                {"title": title, "rating": rating},
            )
            connection.commit()
            print(f"Movie '{title}' updated successfully.")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False