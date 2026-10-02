# Python Movie CLI

A command-line movie database application built with Python. It allows you to manage movies and ratings, perform basic analytics, search and sort movies, and generate a histogram of movie ratings.

## Features

* List all movies
* Add a movie and rating
* Update a movie's rating
* Delete a movie
* Search for movies
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
uv run python movies.py
```

Or using Python directly after installing the dependencies:

```bash
python movies.py
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
