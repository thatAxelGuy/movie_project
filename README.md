# Python Movie CLI

A command-line movie database application built with Python. It allows you to manage movies and ratings, perform basic analytics, search and sort movies, generate a histogram of movie ratings, and find movies using fuzzy search.

## Features

* List all movies with their ID, title, year, and rating
* Add a movie with a title, year, and rating
* Update a movie's rating by ID
* Delete a movie by ID with confirmation
* Search for movies

  * Exact and partial title matching
  * Fuzzy matching using Levenshtein distance
* Display movie statistics

  * Average rating
  * Median rating
  * Highest-rated movie(s)
  * Lowest-rated movie(s)
* Select a random movie
* Sort movies by rating
* Create and save a histogram of movie ratings
* Persist movie data in a JSON file

## Requirements

* Python 3
* `uv` (optional)

## Setup

### Using uv

Install the project dependencies with:

```bash
uv sync
```

### Using pip

Install the dependencies listed in `requirements.txt` with:

```bash
pip install -r requirements.txt
```

Choose **one** of the setup methods above.

## Running the Application

Using `uv`:

```bash
uv run python main.py
```

Or using Python directly after installing the dependencies:

```bash
python main.py
```

## Project Structure

```text
.
├── main.py
├── models.py
├── database.py
├── config.py
├── movies.json
├── requirements.txt
├── README.md
├── uv.lock
└── pyproject.toml
```

### File Responsibilities

* `main.py` — Application entry point and movie management operations
* `models.py` — Movie data structure and type definitions
* `database.py` — Loading and saving movies to JSON
* `config.py` — Application configuration such as the movies data file
* `movies.json` — Persistent movie database

## Movie Data

Each movie contains the following properties:

* **Title** — Movie title
* **Year** — Year the movie was released
* **Rating** — Rating from 0 to 10

Movies are stored using a unique numeric ID:

```text
1. The Shawshank Redemption (1994), Rating: 9.5/10
2. Pulp Fiction (1994), Rating: 8.8/10
```

The data is persisted in `movies.json` so changes are retained between application runs.

## Fuzzy Search

The application uses Levenshtein distance to find movies when the search query contains spelling mistakes.

For example, a search such as:

```text
Gofather
```

can find movies containing similar words such as:

```text
The Godfather
The Godfather: Part II
```

The fuzzy search compares individual words in the query with words in each movie title and uses an edit-distance threshold to determine whether words are similar enough to match.

## Movie Rating Histogram

The application can generate a histogram showing the distribution of movie ratings.

When creating a histogram, you can provide a filename such as:

```text
ratings.png
```

The generated image is saved to the specified location.
