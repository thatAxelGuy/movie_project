"""
A command-line movie database application that allows users
to manage movies and their ratings and perform basic analytics.
"""

from collections.abc import Callable


def list_movies(movies: dict):
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


def add_movie(movies: dict):
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


def update_movie_rating(movies: dict):
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


def run_menu(movies: dict):
    menu_options: dict[str, Callable] = {
        "1": list_movies,
        "2": add_movie,
        "3": update_movie_rating,
    }

    while True:
        print("\n" + "*" * 8 + " Axel's Movie Database " + "*" * 8)
        print("1. View all movies")
        print("2. Add a new movie")
        print("3. Update a movie rating")

        choice = input("Enter your choice (1-6): ")

        if choice in menu_options:
            menu_options[choice](movies)
        elif choice == "6":
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    # Dictionary to store the movies and the rating
    movies = {
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
