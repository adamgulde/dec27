from colorama import Style, Fore

def print_w_dots(string: str, end='\n') -> None:
    """Prints a string with predetermined dot padding after it."""
    for i in range(50-len(string)):
        string += '.'
    print(Fore.GREEN+string, end=Style.RESET_ALL+end)