"""
A command-line movie database application that allows users
to manage movies and their ratings and perform basic analytics.
"""

import random
from collections.abc import Callable


def list_movies(movies: dict[str, float]):
    """
    Lists all the movies in the database along with their ratings.
    """
    print("\n" * 50)  # Clear the console
    print("=" * 40)
    print(f"{len(movies)} movies found in the database.")
    print("List of Movies:")
    print("-" * 40)

    for movie, rating in movies.items():
        print(f"{movie}: {rating}")


def add_movie(movies: dict[str, float]):
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


def update_movie_rating(movies: dict[str, float]):
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


def generate_analytics(movies: dict[str, float]):
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
    print("Movie Analytics:")
    print("-" * 40)
    print(f"Total number of movies: {total_movies}")
    print(f"Average rating: {average_rating:.2f}")
    if len(highest_rated_movies) > 1:
        print(
            f"Highest rated movies: {', '.join(highest_rated_movies)} ({highest_rating})"
        )
    else:
        print(f"Highest rated movie: {highest_rated_movies[0]} ({highest_rating})")
    if len(lowest_rated_movies) > 1:
        print(
            f"Lowest rated movies: {', '.join(lowest_rated_movies)} ({lowest_rating})"
        )
    else:
        print(f"Lowest rated movie: {lowest_rated_movies[0]} ({lowest_rating})")
    print(f"Median rating: {median_rating:.2f}")


def fetch_random_movie(movies: dict[str, float]):
    """
    Fetches and displays a random movie from the database.
    """

    print("\n" * 50)  # Clear the console
    if not movies:
        print("No movies in the database to fetch.")
        return

    random_movie = random.choice(list(movies.items()))
    print(f"Random Movie: {random_movie[0]} with a rating of {random_movie[1]}")


def search_movies(movies: dict[str, float]):
    """
    Search for all movies that match the user input.
    """
    print("\n" * 50)  # Clear the console
    search_query = input("What movie are you looking for?: ")
    search_results = {}

    for movie, rating in movies.items():
        if search_query.lower() in movie.lower():
            search_results[movie] = rating

    print("\n" * 50)  # Clear the console
    print("=" * 40)
    print(f"{len(search_results)} movies found in the database.")
    print("List of Movies:")
    print("-" * 40)

    for movie, rating in search_results.items():
        print(f"{movie}: {rating}")


def sort_movies_by_rating(movies: dict[str, float]):
    """
    Displays movies from highest to lowest rating.
    """
    print("\n" * 50)  # Clear the console
    choice = input("Sort in ascending order (y/n): ")
    descending: bool = True
    if choice.lower() == "y":
        descending = False
    elif choice.lower() == "n":
        descending = True
    else:
        print("Invalid input. Showing in descending order")

    sorted_movies = sorted( 
        movies.items(),
        key=lambda item: item[1],
        reverse=descending
    )

    
    print("=" * 40)
    print(f"{len(movies)} movies found in the database.")
    print("List of Movies:")
    print("-" * 40)
    
    for movie, rating in sorted_movies:
        print(f"{movie}: {rating}")


def delete_movie(movies: dict[str, float]):
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


def run_menu(movies: dict[str, float]):
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
        ("Sort movies by rating", sort_movies_by_rating),
        ("Delete a movie", delete_movie),
        ("Exit", None),
    ]

    while True:
        print("\n" + "*" * 8 + " Axel's Movie Database " + "*" * 8)
        for index, (label, function) in enumerate(menu_options, start=1):
            print(f"{index}. {label}")

        choice = input(f"Enter your choice (1-{len(menu_options)}): ")
        # Convert the user's menu choice to a 0-based list index.
        choice_index = int(choice) - 1 if choice.isdigit() else -1

        if 0 <= choice_index < len(menu_options):
            label, function = menu_options[choice_index]
            if function:
                function(movies)
            else:
                # None indicates the Exit option was selected.
                print("Exiting the application. Goodbye!")
                break
        else:
            print("Invalid choice. Please try again.")


def main():
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
