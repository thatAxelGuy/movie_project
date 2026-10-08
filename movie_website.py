"""Static HTML movie website generator."""

import html

import config
from colors import error, success
from models import Movie

from storage import movie_storage_sql as storage

MOVIE_ITEM_TEMPLATE = """    <li>
      <div class="movie">
        {poster_html}<div class="movie-title">{title}</div>
        <div class="movie-year">{year}</div>
      </div>
    </li>"""


def _build_movie_grid(movies: dict[int, Movie]) -> str:
    """Render the HTML for the movie grid from the stored movies."""
    items = []
    for movie in movies.values():
        poster_url = movie["poster_url"]
        poster_html = (
            ""
            if poster_url == "N/A"
            else f'<img class="movie-poster" src="{html.escape(poster_url)}" alt=""/>'
        )
        items.append(
            MOVIE_ITEM_TEMPLATE.format(
                poster_html=poster_html,
                title=html.escape(movie["title"]),
                year=movie["year"],
            )
        )
    return "\n".join(items)


def generate_website() -> None:
    """Generate a static HTML website listing all movies."""
    movies = storage.list_movies()

    if not movies:
        print("No movies in the database to add to the website.")
        return

    try:
        template = config.TEMPLATE_FILE.read_text()
    except OSError as e:
        print(error(f"Could not read website template: {e}"))
        return

    page = template.replace("__TEMPLATE_TITLE__", "My Movie App").replace(
        "__TEMPLATE_MOVIE_GRID__", _build_movie_grid(movies)
    )

    try:
        config.OUTPUT_HTML_FILE.write_text(page)
    except OSError as e:
        print(error(f"Could not write website file: {e}"))
        return

    print(success(f"Website generated successfully: {config.OUTPUT_HTML_FILE}"))
