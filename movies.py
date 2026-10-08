"""Movie database CLI application."""

from collections.abc import Callable

from colors import error, info, menu, warning
from movie_actions import add_movie, delete_movie, list_movies, update_movie_rating
from movie_analytics import (
    create_rating_histogram,
    fetch_random_movie,
    generate_analytics,
    search_movies,
    sort_movies_by_rating,
)

# import movie_storage
import movie_storage_sql as storage


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
