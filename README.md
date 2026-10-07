# Movie Database

A command-line movie database application built with Python. The application allows you to manage a collection of movies, store them persistently in a JSON file, search and sort movies, and view basic statistics.

## Features

* View all movies
* Add a new movie
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
* Persistent JSON storage
* Colored CLI output for improved readability

## Project Structure

```text
movie_database/
├── movies.py          # CLI, menu, user interaction, and movie operations
├── movie_storage.py   # JSON persistence and database operations
├── movie_utils.py     # Reusable utility functions
├── models.py          # Shared type definitions
├── config.py          # Application configuration
├── colors.py          # CLI color and formatting helpers
├── movies.json        # Persistent movie database
├── requirements.txt   # Python dependencies
├── pyproject.toml     # Project configuration
├── uv.lock            # Dependency lock file
└── README.md          # Project documentation
```

## Data Storage

Movies are stored in `movies.json`.

Each movie has a unique ID and contains:

* `title`
* `year`
* `rating`

Example:

```json
{
    "1": {
        "title": "The Matrix",
        "year": 1999,
        "rating": 8.7
    },
    "2": {
        "title": "Inception",
        "year": 2010,
        "rating": 8.8
    }
}
```

The application converts JSON movie IDs from strings to integers when loading the data.

## Running the Application

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the application with:

```bash
python movies.py
```

## Menu Options

The application provides the following options:

1. **View all movies** — Display all movies with their ID, title, year, and rating.
2. **Add a new movie** — Add a movie after validating its release year and rating.
3. **Update a movie rating** — Select a movie by ID and change its rating.
4. **Show Statistics** — Display rating statistics for the database.
5. **Show a random movie** — Select and display a random movie.
6. **Search movies** — Search by title using exact, partial, and fuzzy matching.
7. **Create a histogram** — Generate a histogram showing the distribution of movie ratings.
8. **Sort movies by rating** — Display movies ordered from highest to lowest rating.
9. **Delete a movie** — Select a movie by ID and permanently remove it from the database.
10. **Exit** — Close the application.

## Architecture

The application separates user interaction from data storage:

### `movies.py`

Handles:

* User input
* Validation
* Menu navigation
* Display formatting
* Search and analytics logic

### `movie_storage.py`

Handles:

* Loading movies from JSON
* Saving movies to JSON
* Adding movies
* Updating movie ratings
* Deleting movies

The storage module does not handle user input or display output.

### `movie_utils.py`

Contains reusable utility functions such as the Levenshtein distance calculation used for fuzzy movie-title searches.

### `models.py`

Contains shared type definitions used throughout the application.

### `config.py`

Contains application configuration such as the location of the JSON database file.

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

* Movie years must be between 1888 and the current year.
* Ratings must be between `0` and `10`.
* Movie IDs must exist before updating or deleting.
* Duplicate movies with the same title and release year are rejected.
* Invalid numeric input is handled without crashing the application.

## Dependencies

The application uses:

* Python
* Colorama
* Matplotlib

See `requirements.txt` for the complete dependency list.
