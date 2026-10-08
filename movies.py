"""Movie database CLI application."""

import random
import os
import requests
from dotenv import load_dotenv
from collections.abc import Callable
from datetime import date

import matplotlib.pyplot as plt
from colors import (
    error,
    success,
    warning,
    info,
    menu,
    rating_formatted,
    bold,
    Fore,
)

# import movie_storage
import movie_storage_sql as storage
from models import Movie
from movie_utils import levenshtein_distance

load_dotenv()


API_KEY = os.getenv("OMDB_API_KEY")

if not API_KEY:
    raise ValueError("OMDB_API_KEY is not set in the environment.")

DATA_URL = "http://www.omdbapi.com/"
POSTER_URL = f"http://img.omdbapi.com/?apikey={API_KEY}&"


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


def _get_movie_year() -> int | None:
    """Prompt for and validate a movie year."""
    while True:

        year_input = input(
            "Enter the year (YYYY) the movie was released (or q to cancel): "
        ).strip()

        if year_input.lower() == "q":
            print(info("Adding movie cancelled."))
            return None

        try:
            year = int(year_input)
            current_year = date.today().year

            if 1888 <= year <= current_year:
                break

            print(
                error(
                    f"Year must be between 1888 and {current_year}. "
                    "Please try again."
                )
            )

        except ValueError:
            print(error("Invalid input. Please enter valid numeric values."))
            continue
    return year


def _get_movie_rating() -> float | None:
    """Prompt for and validate a movie rating."""
    while True:
        rating_input = input(
            "Enter the rating for the movie (0-10) - (or q to cancel): "
        ).strip()

        if rating_input.lower() == "q":
            print(info("Adding movie cancelled."))
            return None

        try:
            rating = float(rating_input)

            if 0 <= rating <= 10:
                break
            print(error("Rating must be between 0 and 10. Please try again!"))

        except ValueError:
            print(error("Please enter a valid rating!"))
    return rating


def get_movie_from_api(imdb_id: str) -> dict | None:
    """Fetch detailed movie data from the OMDb API."""
    try:
        response = requests.get(
            DATA_URL,
            params={
                "apikey": API_KEY,
                "i": imdb_id,
            },
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(error(f"Could not connect to OMDb API: {e}"))
        return None


def search_movies_from_api(title: str) -> dict | None:
    """Search for movies by title in the OMDb API."""
    try:
        response = requests.get(
            DATA_URL,
            params={
                "apikey": API_KEY,
                "s": title,
                "type": "movie",
            },
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(error(f"Could not connect to OMDb API: {e}"))
        return None


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

    movies = storage.list_movies()

    # Check whether movie with the same title already exists in database
    if any(movie["title"].lower() == title.lower() for movie in movies.values()):
        print(error(f"{title} already exists in the database."))
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


def generate_analytics() -> None:
    """Show summary statistics for the movie database."""
    print("\n" * 50)  # Clear the console
    movies = storage.list_movies()

    if not movies:
        print("No movies in the database to analyze.")
        return

    ratings = [movie["rating"] for movie in movies.values()]

    total_movies = len(movies)
    average_rating = sum(ratings) / total_movies
    highest_rating = max(ratings)
    highest_rated_movies = [
        movie["title"] for movie in movies.values() if movie["rating"] == highest_rating
    ]
    lowest_rating = min(ratings)
    lowest_rated_movies = [
        movie["title"] for movie in movies.values() if movie["rating"] == lowest_rating
    ]

    # Calculate the median rating
    ratings.sort()
    if len(ratings) % 2 == 0:
        mid = len(ratings) // 2
        median_rating = (ratings[mid - 1] + ratings[mid]) / 2
    else:
        median_rating = ratings[len(ratings) // 2]

    print("=" * 40)
    print(menu("Movie Analytics:"))
    print("-" * 40)
    print(menu("Total number of movies: " + info(f"{total_movies}")))
    print(menu("Average rating: ") + rating_formatted(average_rating))
    if len(highest_rated_movies) > 1:
        print(
            menu(f"Highest rated movies: {', '.join(highest_rated_movies)} ")
            + rating_formatted(highest_rating)
        )
    else:
        print(
            menu("Highest rated movie: ")
            + Fore.WHITE
            + bold(highest_rated_movies[0])
            + " "
            + rating_formatted(highest_rating)
        )
    if len(lowest_rated_movies) > 1:
        print(
            menu(f"Lowest rated movies: {', '.join(lowest_rated_movies)}")
            + rating_formatted(lowest_rating)
        )
    else:
        print(
            menu("Lowest rated movie: ")
            + Fore.WHITE
            + bold(lowest_rated_movies[0])
            + " "
            + rating_formatted(lowest_rating)
        )
    print(menu("Median rating: " + rating_formatted(median_rating)))


def fetch_random_movie() -> None:
    """Display a random movie from the database."""

    print("\n" * 50)  # Clear the console

    movies = storage.list_movies()

    if not movies:
        print("No movies in the database to fetch.")
        return

    movie = random.choice(list(movies.values()))

    print("=" * 40)
    print(menu("Random Movie:"))
    print("-" * 40)
    print(f"Title: {movie['title']}")
    print(f"Year: {movie['year']}")
    print(f"Rating: {rating_formatted(movie['rating'])}")


def search_movies() -> None:
    """Search the movie database by title using direct and fuzzy matching."""
    print("\n" * 50)  # Clear the console#

    movies = storage.list_movies()

    search_query = input("What movie are you looking for?: ")

    if not search_query:
        print("Please enter a movie title to search for.")
        return

    search_results: dict[int, Movie] = {}

    for movie_id, movie in movies.items():
        title = movie["title"]

        # First, check for an exact or partial match.
        if search_query.lower() in title.lower():
            search_results[movie_id] = movie
        else:
            # If there is no direct match, try fuzzy matching.
            title_words = title.split()
            query_words = search_query.split()

            # Keep track of how many words found a close match
            matches = 0

            for query_word in query_words:

                for title_word in title_words:
                    # Remove punctuation from the ends of words
                    clean_word = title_word.strip(":,!?")
                    clean_query = query_word.strip(":,!?")

                    # Compare the two words using Levenshtein distance.
                    distance = levenshtein_distance(
                        clean_query.lower(), clean_word.lower()
                    )

                    # A distance of 2 or less is considered a fuzzy match.
                    if distance <= 2:
                        matches += 1
                        break

            # Only include the movie if every query word found a match.
            if matches == len(query_words):
                search_results[movie_id] = movie

    print("\n" * 50)  # Clear the console
    print("=" * 40)
    print(f"You searched for {search_query}")
    print(success(f"{len(search_results)}") + " movies found for your search.")
    print("List of Movies:")
    print("-" * 40)

    if not search_results:
        print("No movies found.")
        return

    for movie_id, movie in search_results.items():
        print(
            menu("ID: ")
            + f"{movie_id}. "
            + menu("Title: ")
            + bold(movie["title"])
            + f" ({movie['year']}), "
            + menu("Rating: ")
            + f"({rating_formatted(movie['rating'])}/10)"
        )


def sort_movies_by_rating() -> None:
    """Show movies sorted by rating, highest first."""
    print("\n" * 50)  # Clear the console

    movies = storage.list_movies()

    sorted_movies = sorted(
        movies.items(), key=lambda item: item[1]["rating"], reverse=True
    )

    print("=" * 40)
    print(f"{len(movies)} movies found in the database.")
    print("List of Movies:")
    print("-" * 40)

    for movie_id, movie in sorted_movies:
        title = movie["title"]
        year = movie["year"]
        rating = rating_formatted(movie["rating"])

        print(
            menu("ID: ")
            + f"{movie_id}. "
            + menu("Title: ")
            + bold(title)
            + f" ({year}), "
            + menu("Rating: ")
            + f"({rating}/10)"
        )


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


def create_rating_histogram() -> None:
    """Create a histogram of movie ratings."""
    print("\n" * 50)  # Clear the console

    movies = storage.list_movies()

    if not movies:
        print("No movies in the database to create a histogram.")
        return

    allowed_extensions = (".png", ".jpg", ".jpeg")

    file_name = input("Enter a file name for the histogram(.png): ").strip()

    if not file_name:
        print(error("File name cannot be empty."))
        return

    if not file_name.lower().endswith(allowed_extensions):
        file_name += ".png"

    ratings = [movie["rating"] for movie in movies.values()]

    plt.hist(ratings)
    plt.xlabel("Rating")
    plt.ylabel("Number of Movies")
    plt.title("Movie Ratings")
    plt.savefig(file_name)
    plt.close()

    print(f"Rating histogram saved to {file_name}.")


def run_menu() -> None:
    """Display the main menu and handle user choices."""

    # Each menu item contains a display label and its associated function.
    # Exit has no function, so its value is None.
    menu_options: list[tuple[str, Callable | None]] = [
        (warning("Exit"), None),
        ("View all movies", list_movies),
        ("Add a new movie", add_movie),
        ("Update a movie rating", update_movie_rating),
        ("Show Statistics", generate_analytics),
        ("Show a random movie", fetch_random_movie),
        ("Search movies", search_movies),
        ("Create a histogram", create_rating_histogram),
        ("Sort movies by rating", sort_movies_by_rating),
        (error("Delete a movie"), delete_movie),
    ]

    while True:
        print(menu("\n" + "*" * 8 + " Axel's Movie Database " + "*" * 8))
        for index, (label, function) in enumerate(menu_options, start=0):
            print(f"{index}. {label}")

        choice = input(
            menu(
                "\nEnter your choice "
                + "("
                + info(f"0-{len(menu_options)-1}")
                + menu("):")
            )
        )
        # Convert the user's menu choice to a 0-based list index.
        choice_index = int(choice) if choice.isdigit() else -1

        if 0 <= choice_index < len(menu_options):
            label, function = menu_options[choice_index]
            if function:
                function()
                input(info("\nPress enter to continue..."))
                print("\n" * 50)  # Clear the console
            else:
                # None indicates the Exit option was selected.
                print(warning("Bye!"))
                break
        else:
            print(error("Invalid choice. Please try again."))


def main() -> None:
    """Start the movie database application."""
    storage.init_db()
    run_menu()


if __name__ == "__main__":
    main()
