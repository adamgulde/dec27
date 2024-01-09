# Terminal total width and height: 150x40
# This matches the default Windows terminal size nicely.
WIDTH = 150
HEIGHT = 40
import os
import sys

# Each quadrant is half the width and height of the screen 
rows = int(HEIGHT/2)
cols = int(WIDTH/2)

# Create the quadrants as 2D lists
quadrant1 = [['1' for _ in range(cols)] for _ in range(rows)]
quadrant2 = [['2' for _ in range(cols)] for _ in range(rows)]
quadrant3 = [['3' for _ in range(cols)] for _ in range(rows)]
quadrant4 = [['4' for _ in range(cols)] for _ in range(rows)]

def update_quadrant1_char(x: int, y: int, char: str) -> None:
    quadrant1[y][x] = char

def update_quadrant2_char(x: int, y: int, char: str) -> None:
    quadrant2[y][x] = char

def update_quadrant3_char(x: int, y: int, char: str) -> None:    
    quadrant3[y][x] = char  

def update_quadrant4_char(x: int, y: int, char: str) -> None:
    quadrant4[y][x] = char

def update_quadrant1(quadrant: list[list[str]]) -> None:
    global quadrant1
    quadrant1 = quadrant

def update_quadrant2(quadrant: list[list[str]]) -> None:
    global quadrant2
    quadrant2 = quadrant

def update_quadrant3(quadrant: list[list[str]]) -> None:
    global quadrant3
    quadrant3 = quadrant

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Naive implementation of printing the screen
def print_screen():
    clear_screen()
    print(' ' + '=' * (WIDTH+3))
    for y in range(rows):
        print('||', end='')
        for x in range(2 * cols):
            if x < cols:
                print(quadrant1[y][x], end='')
            elif x == cols:
                print('|' + quadrant2[y][x - cols], end='')
            else:
                print(quadrant2[y][x - cols], end='')
        print('||')
    print(' ' + '-' * (WIDTH+3))
    for y in range(rows):
        print('||', end='')
        for x in range(2 * cols):
            if x < cols:
                print(quadrant3[y][x], end='')
            elif x == cols:
                print('|' + quadrant4[y][x - cols], end='')
            else:
                print(quadrant4[y][x - cols], end='')
        print('||')
    print(' ' + '=' * (WIDTH+3))
    sys.stdout.flush()

print_screen()
# Test 1 - Update all quadrants with different characters
input("This visual test contains flashing images. Press enter to continue...")
for i in range(cols):
    for j in range(rows):
        if(i < cols/2):
            update_quadrant1_char(i, j, 'A')
            update_quadrant2_char(i, j, 'B')
            update_quadrant3_char(i, j, 'C')
            update_quadrant4_char(i, j, 'D')
        else:
            update_quadrant1_char(i, j, 'A')
            update_quadrant2_char(i, j, 'B')
            update_quadrant3_char(i, j, 'C')
            update_quadrant4_char(i, j, 'D')
            update_quadrant1_char(i-cols, j, '1')
            update_quadrant2_char(i-cols, j, '2')
            update_quadrant3_char(i-cols, j, '3')
            update_quadrant4_char(i-cols, j, '4')
        print_screen()
