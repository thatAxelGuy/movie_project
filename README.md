# Python Movie CLI

A command-line movie database application built with Python. It allows you to manage movies and ratings, perform basic analytics, search and sort movies, generate a histogram of movie ratings, and find movies using fuzzy search.

## Features

* List all movies
* Add a movie and rating
* Update a movie's rating
* Delete a movie
* Search for movies

  * Exact and partial matching
  * Fuzzy matching using Levenshtein distance
* Display movie statistics:

  * Average rating
  * Median rating
  * Highest-rated movie(s)
  * Lowest-rated movie(s)
* Select a random movie
* Sort movies by rating
* Create and save a histogram of movie ratings

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
├── requirements.txt
├── README.md
├── uv.lock
└── pyproject.toml
```

## Fuzzy Search

The application uses Levenshtein distance to find movies when the search query contains spelling mistakes.

For example, a search such as:

```text
Gofather
```

can find movies containing a similar word such as:

```text
The Godfather
The Godfather: Part II
```

The fuzzy search compares individual words in the query with words in each movie title and uses an edit-distance threshold to determine whether words are similar enough to match.
