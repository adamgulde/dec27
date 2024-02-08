from colorama import Style, Fore

def print_w_dots(text: str, size: int=50, end: str='\n') -> None:
    """
    Prints a green string with predetermined dot padding after it.
    
    Parameters: 
    text (str): string to pad dots after. 
    size (int): integer of how long the padded string should be. Default 50.
    end (str): value to print immediately at the end of the text (after clearing color formatting). Default newline.

    Returns: 
    None
    """
    for i in range(size-len(text)):
        text += '.'
    print(Fore.GREEN+text, end=Style.RESET_ALL+end)

def get_graphics() -> dict:
    """
    Reads all graphics from ascii.txt into a dictionary.

    Parameters: None

    Returns: 
    Dictionary with the following keys:\n
    - 'help' A page of useful information to the player.
    - 'properties' List of properties in the game.
    - 'divider' ASCII graphic used throughout gameplay, i.e. printing deed information.
    - 'skull' ASCII graphic used on a killed terminal.
    - 'gameboard' The default gameboard. needs to be decoded  with 'unicode_escape' and 'utf-8' 
    - 'help 2' Displays additional information. 
    """

    with open("ascii.txt", encoding='utf-8') as f:
        text = f.read().split("BREAK_TEXT")
    text_dict = {'help': text[0],
                 'properties': text[1],
                 # Use .strip() to remove whitespace if necessary
                 'divider': text[2].lstrip(),
                 'skull': text[3].lstrip(),
                 'gameboard': bytes(text[4].lstrip(), 'utf-8').decode('unicode_escape').encode('latin-1').decode('utf-8'),
                 'help 2': text[5],
                 } 
    return text_dict