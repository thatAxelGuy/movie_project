from colorama import Fore, Style

def error(text) -> str:
    return f"{Fore.RED}{text}{Style.RESET_ALL}"

def success(text) -> str:
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}"

def warning(text) -> str:
    return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"

def info(text) -> str:
    return f"{Fore.CYAN}{text}{Style.RESET_ALL}"

def menu(text) -> str:
    return f"{Fore.BLUE}{text}{Style.RESET_ALL}"

def rating_formatted(rating: float) -> str:
    if rating >= 9:
        return f"{Fore.LIGHTGREEN_EX}{rating:.1f}{Style.RESET_ALL}"

    elif rating >= 5:
        return f"{Fore.YELLOW}{rating:.1f}{Style.RESET_ALL}"

    else:
        return f"{Fore.LIGHTRED_EX}{rating:.1f}{Style.RESET_ALL}"

def bold(text: str) -> str:
    return f"\033[1m{text}\033[0m"