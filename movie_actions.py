"""CRUD menu actions for listing, adding, updating, and deleting movies."""

from colors import bold, error, info, menu, rating_formatted, success, warning
from movie_api import get_movie_from_api, search_movies_from_api

import movie_storage_sql as storage


def list_movies() -> None:
    """
    Lists all the movies in the database along with their ratings.
    """
    movies = storage.list_movies()

    print("\n" * 50)  # Clear the console
    print("=" * 40)
    print(success(f"{len(movies)}") + " movies found in the database.")
    print("List of Movies:")
    print("-" * 40)

    for movie_id, movie in movies.items():
        print(
            menu("ID: ")
            + f"{movie_id}. "
            + menu("Title: ")
            + bold(movie["title"])
            + f" ({movie['year']}), "
            + menu("Rating: ")
            + f"{rating_formatted(movie['rating'])}/10"
        )


def _get_movie_title() -> str | None:
    """Prompt for and validate a movie title."""
    while True:

        title = input("Enter the name of the movie (or q to cancel): ").strip()

        if title.lower() == "q":
            print(info("Adding movie cancelled."))
            return None

        if title:
            break

        print(error("Title can't be empty! Please try again."))
    return title


def _display_movie_search_results(movies: list[dict]) -> None:
    """Print movie search results with numbered choices."""
    print("\n" + menu("Search results"))
    print("-" * 40)

    for index, movie in enumerate(movies, start=1):
        print(
            f"{menu(str(index) + '. ')}" f"{bold(movie['Title'])} " f"({movie['Year']})"
        )


def add_movie() -> None:
    """Add a movie to the database."""
    print("\n" * 50)  # Clear the console

    title = _get_movie_title()
    if title is None:
        return

    search_results = search_movies_from_api(title)

    if search_results is None:
        return

    if search_results.get("Response") == "False":
        print(error(search_results.get("Error", "Movie not found.")))
        return

    movie_list = search_results.get("Search", [])[:5]

    _display_movie_search_results(movie_list)

    while True:
        choice = (
            input(
                "\nEnter q to cancel.\nWhich movie would you like to add "
                f"(1-{len(movie_list)}): "
            )
        ).strip()

        if choice.lower() == "q":
            print(info("Add movie cancelled."))
            return

        try:
            choice = int(choice)
        except ValueError:
            print(error("Please enter a valid number."))
            continue

        if 1 <= choice <= len(movie_list):
            break

        print(error(f"Please enter a number between 1 and {len(movie_list)}."))

    selected_movie = movie_list[choice - 1]

    movie_id = selected_movie.get("imdbID")

    movie = get_movie_from_api(movie_id)

    if movie is None:
        return

    if movie.get("Response") == "False":
        print(error(movie.get("Error", "Movie lookup failed.")))
        return

    movie_title = movie["Title"]
    movie_year = int(movie["Year"][:4])
    movie_rating = float(movie["imdbRating"])
    poster_url = movie.get("Poster", "N/A")

    if storage.movie_exists(movie_title):
        print(
            warning("Movie already exists: ")
            + bold(movie_title)
            + warning(f" ({movie_year})")
        )
        return

    if storage.add_movie(
        title=movie_title, year=movie_year, rating=movie_rating, poster_url=poster_url
    ):
        print(
            success("Movie added: ")
            + bold(movie_title)
            + f" ({movie_year}), "
            + menu("Rating: ")
            + f"({rating_formatted(movie_rating)}/10)"
        )
    else:
        print(error("Failed to save the movie."))


def update_movie_rating() -> None:
    """Update an existing movie rating."""
    print("\n" * 50)  # Clear the console

    movies = storage.list_movies()

    list_movies()
    while True:
        id_input = input(
            "\nEnter the ID of the movie to update (or q to cancel): "
        ).strip()

        if id_input.lower() == "q":
            print(info("Update movie rating cancelled."))
            return

        try:
            movie_id = int(id_input)

            if movie_id not in movies:
                print(
                    error("Movie with ID ")
                    + bold(str(movie_id))
                    + error("does not exist.")
                )
                continue
            break
        except ValueError:
            print(error("Invalid input. Please enter a valid movie id."))

    movie = movies[movie_id]

    print(
        menu("Selected movie: ")
        + bold(movie["title"])
        + f" ({movie['year']}), "
        + menu("Current rating: ")
        + f"({rating_formatted(movie['rating'])}/10)"
    )

    while True:

        rating_input = input(
            "Enter the new rating for the movie (0-10) -" " (or q to cancel): "
        ).strip()

        if rating_input.lower() == "q":
            print(info("Update rating was cancelled."))
            return

        try:

            new_rating = float(rating_input)

            if 0 <= new_rating <= 10:
                break
            print(error("Rating must be between 0 and 10."))

        except ValueError:
            print(error("Invalid input. Please enter a valid rating (0-10)."))

    if storage.update_movie(movie_id, new_rating):
        print(
            success("Rating updated for ")
            + bold(movie["title"])
            + f" to {rating_formatted(new_rating)}/10."
        )
    else:
        print(error("Failed to save the updated rating."))


def delete_movie() -> None:
    """Delete a movie from the database."""
    print("\n" * 50)  # Clear the console
    movies = storage.list_movies()
    list_movies()
    while True:
        id_input = input(
            "Enter the ID of the movie you want to delete " "(or q to cancel): "
        ).strip()

        if id_input.lower() == "q":
            print(info("Delete movie cancelled."))
            return

        try:
            movie_id = int(id_input)

            if movie_id not in movies:
                print(
                    error("Movie with ID ")
                    + bold(str(movie_id))
                    + error(" does not exist.")
                )
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid movie ID.")

    movie = movies[movie_id]

    print(
        menu("Movie to delete: ")
        + bold(movie["title"])
        + f" ({movie['year']}), "
        + menu("Rating: ")
        + f"({rating_formatted(movie['rating'])}/10)"
    )

    while True:

        confirmation = (
            input(warning("Are you sure you want to delete this movie? (y/n): "))
            .strip()
            .lower()
        )

        if confirmation == "y":
            break

        if confirmation == "n":
            print(error("Movie deletion cancelled!"))
            return

        print(error("Please enter y or n."))

    if storage.delete_movie(movie_id):
        print(success("Movie deleted: ") + bold(movie["title"]) + f" ({movie['year']})")
    else:
        print(error("Failed to delete the movie."))
