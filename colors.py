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

def rating_formatted(text) -> str:
    as_float = float(text)

    if as_float >= 9:
        return f"{Fore.LIGHTGREEN_EX}{text}{Style.RESET_ALL}"
    elif as_float >= 5:
        return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"
    else:
        return f"{Fore.LIGHTRED_EX}{text}{Style.RESET_ALL}"