# This file contains the logic for the terminal screen
# Adam Gulde
# Created 1/8/2024
# Updated 1/11/2024

# Terminal total width and height: 150x40
# This matches the default Windows terminal size nicely.
WIDTH = 150
HEIGHT = 40
import os
from colorama import Fore, Style, Back

# Each quadrant is half the width and height of the screen 
rows = HEIGHT//2
cols = WIDTH//2

# Create the quadrants as 2D lists
quadrant1 = ['1' * cols] * rows
quadrant2 = ['2' * cols] * rows
quadrant3 = ['3' * cols] * rows
quadrant4 = ['4' * cols] * rows
active_terminal = 1

def update_quadrant(n: int, data: str):
    # Creates a list of lines from the data string, 
    # and pads each line with spaces to match the width of the screen
    line_list = data.split('\n')
    for i in range(len(line_list)):
            line_list[i] = line_list[i] + ' ' * (cols - len(line_list[i]))
    for i in range(len(line_list), rows):
        line_list.append(' ' * cols)
    match n:
        case 1:
            global quadrant1
            quadrant1 = line_list
        case 2:
            global quadrant2
            quadrant2 = line_list
        case 3:
            global quadrant3
            quadrant3 = line_list
        case 4:
            global quadrant4
            quadrant4 = line_list

# Same as update_quadrant, but does not pad the lines with spaces.
# String must be exactly the right length.
# Useful for color formatting where update_quadrant fails.
def update_quadrant_strictly(n: int, data: str):
    line_list = data.split('\n')
    match n:
        case 1:
            global quadrant1
            quadrant1 = line_list
        case 2:
            global quadrant2
            quadrant2 = line_list
        case 3:
            global quadrant3
            quadrant3 = line_list
        case 4:
            global quadrant4
            quadrant4 = line_list

def update_active_terminal(n: int):
    global active_terminal
    active_terminal = n 

# Writes text over 2nd to last line of the terminal (working line).
def overwrite(text: str):
    print(f'\033[1A\r{text}', end='')

# Naively clears the screen
def clear_screen():
    print(Style.RESET_ALL,end='')
    os.system('cls' if os.name == 'nt' else 'clear')

# This is such an ugly function but it works perfectly
# and I am fairly sure it is very efficient. - 1/11/24
def print_screen():
    # Resets cursor position to top left
    print('\033[1A' * (HEIGHT + 4), end='\r')

    print(Back.BLACK + Fore.LIGHTYELLOW_EX+(Fore.GREEN+'╔' if active_terminal == 1 else '╔')+('═' * (cols))+
          (Fore.GREEN if active_terminal == 1 or active_terminal == 2 else Fore.LIGHTYELLOW_EX) +'╦'
          +(Fore.GREEN if active_terminal == 2 else Fore.LIGHTYELLOW_EX)+('═' * (cols))+'╗' + Fore.LIGHTYELLOW_EX + "   ") # Additional spaces to fill remaining 3 columns
    for y in range(rows):
        print((Fore.GREEN if active_terminal == 1 else Fore.LIGHTYELLOW_EX)+'║', end=Style.RESET_ALL) 
        for x in range(2 * cols):
            if x < cols:
                print(quadrant1[y][x], end='')
            elif x == cols:
                print((Fore.GREEN if active_terminal == 1 or active_terminal == 2 else Fore.LIGHTYELLOW_EX)+'║'+Style.RESET_ALL + quadrant2[y][x - cols], end='')
            else:
                print(quadrant2[y][x - cols], end='')
        print((Fore.GREEN if active_terminal == 2 else Fore.LIGHTYELLOW_EX)+'║'+Style.RESET_ALL + "   ")
    print((Fore.GREEN if active_terminal == 1 or active_terminal == 3 else Fore.LIGHTYELLOW_EX)+'╠' + '═' * (cols)
          +Fore.GREEN + '╬' + (Fore.GREEN if active_terminal == 2 or active_terminal == 4 else Fore.LIGHTYELLOW_EX)+ '═' * (cols) + '╣' + Style.RESET_ALL + "   ")
    for y in range(rows):
        print((Fore.GREEN if active_terminal == 3 else Fore.LIGHTYELLOW_EX)+'║', end=Style.RESET_ALL) 
        for x in range(2 * cols):
            if x < cols:
                print(quadrant3[y][x], end='')
            elif x == cols:
                print((Fore.GREEN if active_terminal == 3 or active_terminal == 4 else Fore.LIGHTYELLOW_EX)+'║'+Style.RESET_ALL + quadrant4[y][x - cols], end='')
            else:
                print(quadrant4[y][x - cols], end='')
        print((Fore.GREEN if active_terminal == 4 else Fore.LIGHTYELLOW_EX)+'║'+Style.RESET_ALL + "   ")
    print((Fore.GREEN if active_terminal == 3 else Fore.LIGHTYELLOW_EX)+'╚' + '═' * (cols) + 
          (Fore.GREEN if active_terminal == 3 or active_terminal == 4 else Fore.LIGHTYELLOW_EX) +'╩'
            + (Fore.GREEN if active_terminal == 4 else Fore.LIGHTYELLOW_EX) + '═' * (cols) + '╝'+ Style.RESET_ALL + "   ")
    # Fills the rest of the terminal
    print(' ' * WIDTH, end='\r')

# Test 1 - Update all quadrants with different characters
def test_1():
    input("This visual test contains flashing images. Press enter to continue...")
    quads = ['', '', '', '']
    for row in range(rows):
        for col in range(cols):
            for i in range(0,4):
                quads[i] += str(i)
                update_quadrant(i+1, quads[i])
            print_screen()
        for i in range(4):
            quads[i] += '\n'