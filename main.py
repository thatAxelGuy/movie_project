"""
A command-line movie database application that allows users
to manage movies and their ratings and perform basic analytics.
"""

import random
import matplotlib.pyplot as plt
from collections.abc import Callable
from colors import error, success, warning, info, menu, rating_formatted


def list_movies(movies: dict[str, float]) -> None:
    """
    Lists all the movies in the database along with their ratings.
    """
    print("\n" * 50)  # Clear the console
    print("=" * 40)
    print(success(f"{len(movies)}") + " movies found in the database.")
    print("List of Movies:")
    print("-" * 40)

    for movie, rating in movies.items():
        print(f"{movie}: " + rating_formatted(rating))


def add_movie(movies: dict[str, float]) -> None:
    """
    Adds a new movie to the database with its rating.
    """
    print("\n" * 50)  # Clear the console
    movie_name = input("Enter the name of the movie: ")

    if movie_name in movies:
        print(f"{movie_name} already exists in the database.")
        return

    try:
        rating = float(input("Enter the rating for the movie (0-10): "))
        if 0 <= rating <= 10:
            movies[movie_name] = rating
            print(f"{movie_name} has been added with a rating of {rating}.")
        else:
            print("Rating must be between 0 and 10.")
    except ValueError:
        print("Invalid input. Please enter a numeric value for the rating.")


def update_movie_rating(movies: dict[str, float]) -> None:
    """
    Updates the rating of an existing movie in the database.
    """
    print("\n" * 50)  # Clear the console
    movie_name = input("Enter the name of the movie to update: ")

    if movie_name not in movies:
        print(f"{movie_name} does not exist in the database.")
        return

    try:
        new_rating = float(input("Enter the new rating for the movie (0-10): "))
        if 0 <= new_rating <= 10:
            movies[movie_name] = new_rating
            print(f"The rating for {movie_name} has been updated to {new_rating}.")
        else:
            print("Rating must be between 0 and 10.")
    except ValueError:
        print("Invalid input. Please enter a numeric value for the rating.")


def generate_analytics(movies: dict[str, float]) -> None:
    """
    Generates and displays analytics about the movies in the database.
    """
    print("\n" * 50)  # Clear the console
    if not movies:
        print("No movies in the database to analyze.")
        return

    total_movies = len(movies)
    average_rating = sum(movies.values()) / total_movies
    highest_rating = max(movies.values())
    highest_rated_movies = [
        movie for movie, rating in movies.items() if rating == highest_rating
    ]
    lowest_rating = min(movies.values())
    lowest_rated_movies = [
        movie for movie, rating in movies.items() if rating == lowest_rating
    ]

    # Calculate the median rating
    ratings = list(movies.values())
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
    print(menu("Average rating: ") + rating_formatted(f"{average_rating:.2f}"))
    if len(highest_rated_movies) > 1:
        print(
            menu(f"Highest rated movies: {', '.join(highest_rated_movies)} ") 
            + rating_formatted(highest_rating)
        )
    else:
        print(menu(f"Highest rated movie: {highest_rated_movies[0]}") 
              + rating_formatted(f" {highest_rating}"))
    if len(lowest_rated_movies) > 1:
        print(
            menu(f"Lowest rated movies: {', '.join(lowest_rated_movies)}" )
            + rating_formatted(f" {lowest_rating}")
        )
    else:
        print(
            menu(f"Lowest rated movie: {lowest_rated_movies[0]}") 
            + rating_formatted( f" {lowest_rating}")
        )
    print(menu("Median rating: " + rating_formatted(f" {median_rating:.2f}")))


def fetch_random_movie(movies: dict[str, float]) -> None:
    """
    Fetches and displays a random movie from the database.
    """

    print("\n" * 50)  # Clear the console
    if not movies:
        print("No movies in the database to fetch.")
        return

    random_movie = random.choice(list(movies.items()))
    print(f"Random Movie: {random_movie[0]} with a rating of {random_movie[1]}")


def levenshtein_distance(word1: str, word2: str) -> int:
    """ Calculates the Levenshtein distance between two words. 
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


def search_movies(movies: dict[str, float]) -> None:
    """Searches the movie database using an exact, partial, or fuzzy match.

    Exact and partial matches are checked first. If no direct match is found,
    the search uses Levenshtein distance to find movie titles containing words
    that are sufficiently similar to the query words.
    """
    print("\n" * 50)  # Clear the console
    search_query = input("What movie are you looking for?: ")
    search_results = {}

    for movie, rating in movies.items():

        # First, check for an exact or partial match.
        # This handles searches such as "star wars" or "dark knight".
        if search_query.lower() in movie.lower():
            search_results[movie] = rating
        else:
            # If there is no direct match, try fuzzy matching.
            # Split the movie title and search query into individual words.
            title_words = movie.split()
            query_words = search_query.split()

            # Keep track of how many words found a close match
            matches = 0

            for query_word in query_words:

                for title_word in title_words:
                    # Remove punctuation from the ends of words so that
                    # "Godfather:" can still match "Godfather".
                    clean_word = title_word.strip(":")
                    clean_query = query_word.strip(":")

                    # Compare the two words using Levenshtein distance.
                    # # A distance of 2 or less is considered a fuzzy match.
                    distance = levenshtein_distance(
                        clean_query.lower(), clean_word.lower()
                    )

                    if distance <= 2:
                        matches += 1
                        # Stop checking title words once this query word
                        # has found a sufficiently similar match.
                        break

            # Only include the movie if every query word found a match.
            if matches == len(query_words):
                search_results[movie] = rating

    print("\n" * 50)  # Clear the console
    print("=" * 40)
    print(f"You searched for {search_query}")
    print(f"success({len(search_results)}movies) found for your search.")
    print("List of Movies:")
    print("-" * 40)

    for movie, rating in search_results.items():
        print(f"{movie}: {rating}")


def sort_movies_by_rating(movies: dict[str, float]) -> None:
    """
    Displays movies from highest to lowest rating.
    """
    print("\n" * 50)  # Clear the console

    sorted_movies = sorted(movies.items(), key=lambda item: item[1], reverse=True)

    print("=" * 40)
    print(f"{len(movies)} movies found in the database.")
    print("List of Movies:")
    print("-" * 40)

    for movie, rating in sorted_movies:
        print(f"{movie}: {rating}")


def delete_movie(movies: dict[str, float]) -> None:
    """
    Deletes a movie from the database.
    """
    print("\n" * 50)  # Clear the console
    movie_name = input("Enter the name of the movie to delete: ")

    if movie_name in movies:
        del movies[movie_name]
        print(f"{movie_name} has been deleted from the database.")
    else:
        print(f"{movie_name} does not exist in the database.")


def create_rating_histogram(movies: dict[str, float]) -> None:
    """
    Creates a histogram of movie ratings.
    """
    print("\n" * 50)  # Clear the console
    if not movies:
        print("No movies in the database to create a histogram.")
        return

    file_name = input("Enter a file name to save the rating histogram to: ")

    if file_name == "":
        print("File name cannot be empty.")
        return

    ratings = list(movies.values())

    plt.hist(ratings)
    plt.savefig(file_name)


def run_menu(movies: dict[str, float]) -> None:
    """
    Displays the main menu and handles user selections until the user exits.
    """

    # Each menu item contains a display label and its associated function.
    # Exit has no function, so its value is None.
    menu_options: list[tuple[str, Callable | None]] = [
        ("View all movies", list_movies),
        ("Add a new movie", add_movie),
        ("Update a movie rating", update_movie_rating),
        ("Show Statistics", generate_analytics),
        ("Show a random movie", fetch_random_movie),
        ("Search movies", search_movies),
        ("Create a histogram", create_rating_histogram),
        ("Sort movies by rating", sort_movies_by_rating),
        (error("Delete a movie"), delete_movie),
        (warning("Exit"), None),
    ]

    while True:
        print(menu("\n" + "*" * 8 + " Axel's Movie Database " + "*" * 8))
        for index, (label, function) in enumerate(menu_options, start=1):
            print(f"{index}. {label}")

        choice = input(
            menu("\nEnter your choice " 
                 + "(" + info(f"1-{len(menu_options)}")  + menu("):")))
        # Convert the user's menu choice to a 0-based list index.
        choice_index = int(choice) - 1 if choice.isdigit() else -1

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
            print("Invalid choice. Please try again.")


def main() -> None:
    """
    Initializes the movie database and starts the main menu.
    """
    # Dictionary to store the movies and the rating
    movies: dict[str, float] = {
        "The Shawshank Redemption": 9.5,
        "Pulp Fiction": 8.8,
        "The Room": 3.6,
        "The Godfather": 9.2,
        "The Godfather: Part II": 9.0,
        "The Dark Knight": 9.0,
        "12 Angry Men": 8.9,
        "Everything Everywhere All At Once": 8.9,
        "Forrest Gump": 8.8,
        "Star Wars: Episode V": 8.7,
    }

    run_menu(movies)


if __name__ == "__main__":
    main()
