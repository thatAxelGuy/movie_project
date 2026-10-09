"""Analytics and reporting menu actions."""

import random

import matplotlib.pyplot as plt

from colors import Fore, bold, error, info, menu, rating_formatted, success
from models import MovieWithNote
from movie_utils import levenshtein_distance

from storage import movie_storage_sql as storage


def generate_analytics(user_id: str) -> None:
    """Show summary statistics for the movie database."""
    print("\n" * 50)  # Clear the console
    movies = storage.list_user_movies(user_id)

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


def fetch_random_movie(user_id: str) -> None:
    """Display a random movie from the database."""

    print("\n" * 50)  # Clear the console

    movies = storage.list_user_movies(user_id)

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


def search_movies(user_id: str) -> None:
    """Search the movie database by title using direct and fuzzy matching."""
    print("\n" * 50)  # Clear the console#

    movies = storage.list_user_movies(user_id)

    search_query = input("What movie are you looking for?: ")

    if not search_query:
        print("Please enter a movie title to search for.")
        return

    search_results: dict[int, MovieWithNote] = {}

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


def sort_movies_by_rating(user_id: str) -> None:
    """Show movies sorted by rating, highest first."""
    print("\n" * 50)  # Clear the console

    movies = storage.list_user_movies(user_id)

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


def create_rating_histogram(user_id: str) -> None:
    """Create a histogram of movie ratings."""
    print("\n" * 50)  # Clear the console

    movies = storage.list_user_movies(user_id)

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
