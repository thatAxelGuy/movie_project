# Movie Database

A command-line movie database application built with Python. The application allows you to manage a collection of movies, fetches movie details from the OMDb API, stores them persistently in a SQLite database, and lets you search, sort, and view basic statistics.

## Features

* View all movies
* Add a new movie by searching the OMDb API by title and picking from the results
* Update a movie's rating
* Delete a movie by ID
* Search movies by title

  * Exact and partial title matching
  * Fuzzy matching using Levenshtein distance
* Show movie statistics

  * Average rating
  * Highest-rated movie(s)
  * Lowest-rated movie(s)
  * Median rating
* Fetch a random movie
* Sort movies by rating
* Create a rating histogram
* Persistent SQLite storage
* Colored CLI output for improved readability

## Project Structure

```text
movie_database/
├── movies.py              # Entry point: menu loop and main
├── movie_api.py           # OMDb API client (search, lookup) and API key setup
├── movie_actions.py        # CRUD menu actions: list, add, update, delete
├── movie_analytics.py       # Read-only menu actions: stats, random, search, sort, histogram
├── movie_storage_sql.py    # SQLAlchemy + SQLite persistence (live storage backend)
├── movie_storage.py        # Legacy JSON persistence (unused, kept for reference)
├── movie_utils.py          # Reusable utility functions (e.g. Levenshtein distance)
├── models.py               # Shared type definitions
├── config.py                # Application configuration (DB URL, legacy JSON path)
├── colors.py                # CLI color and formatting helpers
├── movies.db                 # SQLite movie database (live storage)
├── movies.json              # Legacy JSON movie database (unused)
├── .env                      # OMDB_API_KEY (not committed)
├── requirements.txt         # Python dependencies
├── pyproject.toml           # Project configuration
├── uv.lock                   # Dependency lock file
└── README.md                 # Project documentation
```

## Data Storage

Movies are stored in a SQLite database (`movies.db`), accessed through `movie_storage_sql.py` via SQLAlchemy.

Each movie has a unique ID and contains:

* `title`
* `year`
* `rating`
* `poster_url`

The older `movie_storage.py` (JSON-backed, `movies.json`) implementation is left in place but not active — its function signatures have drifted from the SQL version and it predates the `poster_url` field.

## Running the Application

Install the required dependencies:

```bash
uv sync
```

(or `pip install -r requirements.txt`)

Create a `.env` file in the project root with your OMDb API key:

```text
OMDB_API_KEY=your_key_here
```

Run the application with:

```bash
uv run movies.py
```

(or `python movies.py`)

## Menu Options

The application provides the following options:

1. **View all movies** — Display all movies with their ID, title, year, and rating.
2. **Add a new movie** — Search OMDb by title, pick from up to 5 results, and save the matched movie's title, year, rating, and poster.
3. **Update a movie rating** — Select a movie by ID and change its rating.
4. **Show Statistics** — Display rating statistics for the database.
5. **Show a random movie** — Select and display a random movie.
6. **Search movies** — Search by title using exact, partial, and fuzzy matching.
7. **Create a histogram** — Generate a histogram showing the distribution of movie ratings.
8. **Sort movies by rating** — Display movies ordered from highest to lowest rating.
9. **Delete a movie** — Select a movie by ID and permanently remove it from the database.
0. **Exit** — Close the application.

## Architecture

The application is split into a thin entry point and three focused modules, all going through a storage module rather than touching the database directly:

### `movies.py`

The entry point: the menu loop (`run_menu`) and `main`. Wires together the other modules and contains no business logic of its own.

### `movie_api.py`

The OMDb HTTP client: `search_movies_from_api`, `get_movie_from_api`, plus the API key/env setup and the `ValueError` guard raised if `OMDB_API_KEY` is missing.

### `movie_actions.py`

CRUD menu actions and their input-prompt validation: `list_movies`, `add_movie`, `update_movie_rating`, `delete_movie`.

### `movie_analytics.py`

Read-only analytics/search/reporting menu actions: `generate_analytics`, `fetch_random_movie`, `search_movies`, `sort_movies_by_rating`, `create_rating_histogram`.

### `movie_storage_sql.py`

Handles all database access: listing, adding, updating, and deleting movies in SQLite via SQLAlchemy. Does not handle user input or display output.

### `movie_utils.py`

Contains reusable utility functions such as the Levenshtein distance calculation used for fuzzy movie-title searches.

### `models.py`

Contains shared type definitions used throughout the application.

### `config.py`

Contains application configuration such as the database URL and the legacy JSON file path.

## Search

Movie titles can be searched using:

* Exact matches
* Partial matches
* Fuzzy matching

Fuzzy matching uses **Levenshtein distance** to find titles even when the search contains small spelling mistakes.

For example:

```text
Search: Incepton
Result: Inception
```

## Validation

The application validates user input before modifying the database.

* Ratings must be between `0` and `10`.
* Movie IDs must exist before updating or deleting.
* A movie with the same title (case-insensitive) already in the database is rejected when adding.
* Invalid numeric input is handled without crashing the application.

## Dependencies

The application uses:

* Python
* Colorama
* Matplotlib
* Requests
* python-dotenv
* SQLAlchemy

See `requirements.txt` for the complete dependency list.
