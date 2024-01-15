from colorama import Style, Fore

def print_w_dots(string: str, end='\n') -> None:
    """Prints a string with predetermined dot padding after it."""
    for i in range(50-len(string)):
        string += '.'
    print(Fore.GREEN+string, end=Style.RESET_ALL+end)

# Cool fonts generated here: https://patorjk.com/software/taag/
# https://stackoverflow.com/questions/4020539/process-escape-sequences-in-a-string-in-python
def get_graphics() -> dict:
    global text_dict

    with open("ascii.txt", encoding='utf-8') as f:
        text = f.read().split("BREAK_TEXT")
    text_dict = {'help': text[0],
                 'properties': text[1],
                 # Use .strip() to remove whitespace if necessary
                 'divider': text[2].lstrip(),
                 'skull': text[3].lstrip(),
                 'gameboard': bytes(text[4].lstrip(), 'utf-8').decode('unicode_escape').encode('latin-1').decode('utf-8'),
                 } 
    return text_dict