import os
import socket
from time import sleep
from colorama import Fore, Style, Back
import style as s
import screenspace as ss
import modules as m

game_running = False
text_dict = {}
active_terminal = 1

# Grab text from ascii.txt and split into dictionary

# Cool fonts generated here: https://patorjk.com/software/taag/
def get_graphics() -> dict:
    global text_dict

    with open("ascii.txt") as f:
        text = f.read().split("BREAK_TEXT")
    text_dict = {'help': text[0],
                 'properties': text[1],
                 # Use .strip() to remove whitespace if necessary
                 'divider': text[2]
                 } 
    return text_dict

def initialize():
    os.system("cls")
    print("Welcome to Terminal Monopoly, Player!")
    s.print_w_dots("Initializing client socket connection")     
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    ADDRESS = input("Enter Host IP: ")
    PORT = input("Enter Host Port: ")
    s.print_w_dots("Press enter to connect to the server...", end='')
    input()
    try:
        client_socket.connect((ADDRESS, int(PORT)))
        print(Fore.BLUE+"Connection successful!"+Style.RESET_ALL)
    except:
        n = input(Fore.RED+"Connection failed. Type 'exit' to quit or press enter to try again.\n"+Style.RESET_ALL)
        if n == "exit":
            quit()
        else:
            initialize()
    
def communicate(sock: socket.socket) -> None:
    message = sock.recv(1024).decode('ascii')
    if message == "exit":
        sock.close()
        quit()
    print(message)

# Display all information and commands available to the user, in quadrant 2.
def print_help() -> None:
    ss.update_quadrant(active_terminal, text_dict.get('help'))
    ss.print_screen()

def calculate() -> None:
    # Initial comment in active terminal
    ss.update_quadrant(active_terminal, "Enter a single operation equation:")
    ss.print_screen()
    # All other work is done on the work line (bottom of the screen)
    ss.update_quadrant(active_terminal, m.calculator())
    ss.print_screen()

def list_properties() -> None:
    ss.update_quadrant(active_terminal, text_dict.get('properties'))
    ss.print_screen()

def set_terminal(n: int) -> None:
    global active_terminal
    active_terminal = n
    ss.update_active_terminal(n)
    ss.print_screen()

def get_input() -> str:
    stdIn = ""
    while(stdIn != "exit"):
        stdIn = input(Back.BLACK + Back.LIGHTWHITE_EX+Fore.BLACK+'\r').lower()
        if stdIn == "help":
            print_help()
        elif stdIn == "calc":
            calculate()
        elif stdIn == "list":
            list_properties()
        elif stdIn.startswith("dance"):
            try: 
                for i in range(int(stdIn[6:])):
                    for j in range(4):
                        set_terminal(j+1)
                        sleep(0.05)
            except:
                ss.overwrite(Style.RESET_ALL + Fore.RED + "Something went wrong.")
        elif stdIn.startswith("term "):
            # Short circuiting! I feel smart.
            if(len(stdIn) == 6 and stdIn[5].isdigit() and 5 > int(stdIn.split(" ")[1]) > 0):
                set_terminal(int(stdIn.strip().split(" ")[1]))
                ss.print_screen()
                ss.overwrite(Style.RESET_ALL + Fore.GREEN + "\nActive terminal set to " + str(active_terminal) + ".")
            else:
                ss.overwrite(Style.RESET_ALL + Fore.RED + "Include a number between 1 and 4 (inclusive) after 'term' to set the active terminal.")
            pass
        elif stdIn.startswith("deed"):
            if(len(stdIn) > 4):
                ss.update_quadrant(active_terminal, m.deed(stdIn[5:]))
                ss.print_screen()
        elif stdIn == "test1":
            ss.update_quadrant_strictly(1, m.deed())
            ss.print_screen()
        elif stdIn == "exit" or stdIn == "":
            pass
        else:
            ss.overwrite('\n' + ' ' * ss.WIDTH)
            ss.overwrite(Style.RESET_ALL + Fore.RED + "Invalid command. Type 'help' for a list of commands.")
    if stdIn == "exit" and game_running:
        ss.overwrite('\n' + ' ' * ss.WIDTH)
        ss.overwrite(Fore.RED + "\nYou are still in a game!")
        get_input()

if __name__ == "__main__":
    get_graphics()
    initialize()
    # Prints help to user in quadrant 2 to begin.
    ss.update_quadrant(2, text_dict.get('help'))
    ss.print_screen()
    get_input()
    s.print_w_dots("Goodbye!")
