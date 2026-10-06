"""
A command-line movie database application that allows users
to manage movies and their ratings and perform basic analytics.
"""

import random
import matplotlib.pyplot as plt
from collections.abc import Callable
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
from database import load_movies, save_movies
from datetime import date
from models import Movie

MOVIES_FILE = "movies.json"


def list_movies(movies: dict[int, Movie]) -> None:
    """
    Lists all the movies in the database along with their ratings.
    """
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
            + f"({rating_formatted(movie['rating'])}/10)"
        )


def add_movie(movies: dict[int, Movie]) -> None:
    """
    Adds a new movie to the database with its rating.
    """
    print("\n" * 50)  # Clear the console
    title = input("Enter the name of the movie: ")

    try:
        year = int(input("Enter the year (YYYY) the movie was released: "))

        current_year = date.today().year
        if not 1888 <= year <= current_year:
            print("Invalid year.")
            return

        # Check whether movie with the same title already exists in database
        if any(
            movie["title"].lower() == title.lower() and movie["year"] == year
            for movie in movies.values()
        ):
            print(f"{title} ({year}) already exists in the database.")
            return

        rating = float(input("Enter the rating for the movie (0-10): "))

        if not 0 <= rating <= 10:
            print("Rating must be between 0 and 10.")
            return

        movie_id = max(movies, default=0) + 1

        movies[movie_id] = {
            "title": title,
            "rating": rating,
            "year": year,
        }

        save_movies(MOVIES_FILE, movies)
        print(
            success("Movie added: ")
            + bold(title)
            + f" ({year}), "
            + menu("Rating: ")
            + f"({rating_formatted(rating)}/10)"
        )

    except ValueError:
        print("Invalid input. Please enter valid numeric values.")


def update_movie_rating(movies: dict[int, Movie]) -> None:
    """
    Updates the rating of an existing movie in the database.
    """
    print("\n" * 50)  # Clear the console

    list_movies(movies)

    try:
        movie_id = int(input("\nEnter the ID of the movie to update: "))

        if movie_id not in movies:
            print(f"Movie with ID {movie_id} does not exist.")
            return

        movie = movies[movie_id]

        print(
            menu("Selected movie: ")
            + bold(movie["title"])
            + f" ({movie['year']}), "
            + menu("Current rating: ")
            + f"({rating_formatted(movie['rating'])}/10)"
        )

        new_rating = float(input("Enter the new rating for the movie (0-10): "))

        if not 0 <= new_rating <= 10:
            print("Rating must be between 0 and 10.")
            return

        movie["rating"] = new_rating
        save_movies(MOVIES_FILE, movies)

        print(
            f"The rating for {movie['title']} "
            f"has been updated to {rating_formatted(new_rating)}."
        )

    except ValueError:
        print("Invalid input. Please enter a valid ID and rating.")


def generate_analytics(movies: dict[int, Movie]) -> None:
    """
    Generates and displays analytics about the movies in the database.
    """
    print("\n" * 50)  # Clear the console
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


def fetch_random_movie(movies: dict[int, Movie]) -> None:
    """
    Fetches and displays a random movie from the database.
    """

    print("\n" * 50)  # Clear the console

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


def levenshtein_distance(word1: str, word2: str) -> int:
    """Calculates the Levenshtein distance between two words.
    The distance represents the minimum number of single-character
    insertions, deletions, or substitutions needed to transform one word into the other.

    Returns: int: The minimum number of edits required.
    """
    # [0] * (len(word2) + 1) = number of columns in matrix
    # range(len(word1) + 1) = number of rows in matrix
    matrix = [[0] * (len(word2) + 1) for i in range(len(word1) + 1)]

    for i in range(len(matrix[0])):
        matrix[0][i] = i  # Initialize row 0

    for j in range(len(matrix)):
        matrix[j][0] = j  # Initialize column 0

    for i in range(1, len(matrix)):
        for j in range(1, len(matrix[0])):
            if word1[i - 1] == word2[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1]
            else:
                matrix[i][j] = min(
                    (matrix[i - 1][j] + 1),  # delete
                    (matrix[i][j - 1] + 1),  # insert
                    (matrix[i - 1][j - 1] + 1),  # replace
                )

    return matrix[-1][-1]


def search_movies(movies: dict[int, Movie]) -> None:
    """Searches the movie database using an exact, partial, or fuzzy match.

    Exact and partial matches are checked first. If no direct match is found,
    the search uses Levenshtein distance to find movie titles containing words
    that are sufficiently similar to the query words.
    """
    print("\n" * 50)  # Clear the console
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
    print(f"success({len(search_results)}movies) found for your search.")
    print("List of Movies:")
    print("-" * 40)

    if not search_results:
        print("No movies found.")
        return

    for movie_id, movie in search_results.items():
        print(
            f"{movie_id}. {movie['title']} "
            f"({movie['year']}): "
            f"{rating_formatted(movie['rating'])}"
        )


def sort_movies_by_rating(movies: dict[int, Movie]) -> None:
    """
    Displays movies from highest to lowest rating.
    """
    print("\n" * 50)  # Clear the console

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


def delete_movie(movies: dict[int, Movie]) -> None:
    """
    Deletes a movie from the database.
    """
    print("\n" * 50)  # Clear the console
    list_movies(movies)
    try:
        movie_id = int(input("Enter the ID of the movie you want to delete: "))

        if movie_id not in movies:
            print(
                error("Movie with ID ")
                + bold(str(movie_id))
                + error(" does not exist.")
            )
            return

        movie = movies[movie_id]

        print(
            menu("Movie to delete: ")
            + bold(movie["title"])
            + f" ({movie['year']}), "
            + menu("Rating: ")
            + f"({rating_formatted(movie['rating'])}/10)"
        )

        confirmation = input(
            warning("Are you sure you want to delete this movie? (y/n): ")
        )

        if confirmation.lower() != "y":
            print(error("Movie deletion cancelled!"))
            return

        del movies[movie_id]

        save_movies(MOVIES_FILE, movies)

        print(success("Movie deleted: ") + bold(movie["title"]) + f" ({movie['year']})")

    except ValueError:
        print("Invalid input. Please enter a valid movie ID.")


def create_rating_histogram(movies: dict[int, Movie]) -> None:
    """
    Creates a histogram of movie ratings.
    """
    print("\n" * 50)  # Clear the console
    if not movies:
        print("No movies in the database to create a histogram.")
        return

    allowed_extensions = (".png", ".jpg", ".jpeg")

    file_name = input("Enter a file name for the histogram(.png): ")

    if file_name == "":
        print("File name cannot be empty.")
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


def run_menu(movies: dict[int, Movie]) -> None:
    """
    Displays the main menu and handles user selections until the user exits.
    """

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
                function(movies)
                input(info("\nPress enter to continue..."))
                print("\n" * 50)  # Clear the console
            else:
                # None indicates the Exit option was selected.
                print(warning("Exiting the application. Goodbye!"))
                break
        else:
            print(error("Invalid choice. Please try again."))


def main() -> None:
    """
    Initializes the movie database and starts the main menu.
    """
    movies: dict[int, Movie] = load_movies(MOVIES_FILE)
    run_menu(movies)


if __name__ == "__main__":
    main()
