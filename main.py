"""
A command-line movie database application that allows users
to manage movies and their ratings and perform basic analytics.
"""


def list_movies(movies: dict):
    """
    Lists all the movies in the database along with their ratings.
    """
    print("\nList of Movies:")
    for movie, rating in movies.items():
        print(f"{movie}: {rating}")


def run_menu(movies: dict):
    menu_options = {
        "1": list_movies,
    }

    while True:
        print("\n" + "*" * 8 + " Axel's Movie Database " + "*" * 8)
        print("1. View all movies")

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
