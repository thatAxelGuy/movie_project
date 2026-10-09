"""Movie database CLI application."""

from collections.abc import Callable
from functools import partial

from colors import error, info, menu, warning
from movie_actions import add_movie, delete_movie, list_movies, update_movie_notes
from movie_analytics import (
    create_rating_histogram,
    fetch_random_movie,
    generate_analytics,
    search_movies,
    sort_movies_by_rating,
)
from movie_website import generate_website

# from storage import movie_storage
from storage import movie_storage_sql as storage


def _select_user() -> tuple[str, str] | None:
    """Show the startup screen and return the selected (user_id, user_name).

    Returns None if the user chooses to quit.
    """
    print("\n" * 50)  # Clear the console
    print(menu("\n" + "*" * 8 + " Welcome to the Movie Database " + "*" * 8))
    print(info("Select a profile below, create a new one, or quit.\n"))

    users = storage.list_users()  # list[tuple[str, str]] of (id, name)

    # index 0 = Quit, matching run_menu's convention of an exit-like action at the top
    options: list[tuple[str, str | None]] = [(warning("Quit"), None)]
    options.extend((name, user_id) for user_id, name in users)
    options.append(("Create a new user", "NEW"))

    while True:
        for index, (label, _) in enumerate(options):
            print(f"{index}. {label}")

        choice = input(
            menu("\nEnter your choice (" + info(f"0-{len(options) - 1}") + menu("): "))
        )
        choice_index = int(choice) if choice.isdigit() else -1

        if not (0 <= choice_index < len(options)):
            print(error("Invalid choice. Please try again."))
            continue

        if choice_index == 0:
            return None

        label, value = options[choice_index]

        if value == "NEW":
            name = input(menu("Enter a username for the new profile: ")).strip()
            if not name:
                print(error("Username can't be empty. Please try again."))
                continue
            user_id = storage.create_user(name)
            if user_id is None:
                print(
                    error(f"A user named {name} already exists. ")
                    + info("Pick it from the list or choose another name.")
                )
                continue
            print(info(f"Welcome, {name}! A new profile was created for you."))
            return user_id, name

        print(info(f"Welcome back, {label}!"))
        assert value is not None
        return value, label


def run_menu(user_id: str, user_name: str) -> None:
    """Display the main menu and handle user choices."""

    # Each menu item contains a display label and its associated function.
    # Exit has no function, so its value is None.
    menu_options: list[tuple[str, Callable | None]] = [
        (warning("Exit"), None),
        ("View all movies", partial(list_movies, user_id)),
        ("Add a new movie", partial(add_movie, user_id)),
        ("Update movie notes", partial(update_movie_notes, user_id)),
        ("Show Statistics", partial(generate_analytics, user_id)),
        ("Show a random movie", partial(fetch_random_movie, user_id)),
        ("Search movies", partial(search_movies, user_id)),
        ("Create a histogram", partial(create_rating_histogram, user_id)),
        ("Sort movies by rating", partial(sort_movies_by_rating, user_id)),
        ("Generate website", partial(generate_website, user_id, user_name)),
        (error("Delete a movie"), partial(delete_movie, user_id)),
    ]

    while True:
        print(menu("\n" + "*" * 8 + f" {user_name}'s Movie Database " + "*" * 8))
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

    selection = _select_user()
    if selection is None:
        print(warning("Bye!"))
        return

    user_id, user_name = selection
    run_menu(user_id, user_name)


if __name__ == "__main__":
    main()
