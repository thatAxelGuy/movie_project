"""Static HTML movie website generator."""

import html
import re

import config
from colors import error, success
from models import MovieWithNote

from storage import movie_storage_sql as storage

MOVIE_ITEM_TEMPLATE = """    <li>
      <div class="movie">
        {poster_html}<div class="movie-title">{title}</div>
        <div class="movie-year">{year}</div>
        {note_html}
      </div>
    </li>"""


def _build_movie_grid(movies: dict[int, MovieWithNote]) -> str:
    """Render the HTML for the movie grid from the stored movies."""
    items = []
    for movie in movies.values():
        poster_url = movie["poster_url"]
        poster_html = (
            ""
            if poster_url == "N/A"
            else f'<img class="movie-poster" src="{html.escape(poster_url)}" alt=""/>'
        )
        note = movie["note"]
        note_html = (
            ""
            if note == "N/A"
            else f'<div class="movie-note">"{html.escape(note)}"</div>'
        )
        items.append(
            MOVIE_ITEM_TEMPLATE.format(
                poster_html=poster_html,
                title=html.escape(movie["title"]),
                year=movie["year"],
                note_html=note_html,
            )
        )
    return "\n".join(items)


def _safe_filename(user_name: str) -> str:
    """Sanitize a username into a safe filename component."""
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", user_name)
    return safe or "user"


def generate_website(user_id: str, user_name: str) -> None:
    """Generate a static HTML website listing the given user's movies."""
    movies = storage.list_user_movies(user_id)

    if not movies:
        print("You have no movies in your list to add to the website.")
        return

    try:
        template = config.TEMPLATE_FILE.read_text()
    except OSError as e:
        print(error(f"Could not read website template: {e}"))
        return

    title = f"{html.escape(user_name)}'s Movie App"
    page = template.replace("__TEMPLATE_TITLE__", title).replace(
        "__TEMPLATE_MOVIE_GRID__", _build_movie_grid(movies)
    )

    output_file = config.STATIC_DIR / f"{_safe_filename(user_name)}.html"

    try:
        output_file.write_text(page)
    except OSError as e:
        print(error(f"Could not write website file: {e}"))
        return

    print(success(f"Website generated successfully: {output_file}"))
