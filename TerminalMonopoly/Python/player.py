import os
import socket
from time import sleep
from colorama import Fore, Style, Back
import style as s
import screenspace as ss
from modules import PlayerModules as m

game_running = False
text_dict = {}
active_terminal = 1
sockets = (socket.socket, socket.socket)
ADDRESS = ""
PORT = 0

# Grab text from ascii.txt and split into dictionary
def get_graphics():
    global text_dict
    text_dict = s.get_graphics()

def initialize():
    global sockets, ADDRESS, PORT
    os.system("cls")
    print("Welcome to Terminal Monopoly, Player!")
    s.print_w_dots("Initializing client socket connection")     
    client_receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    client_sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockets = (client_receiver, client_sender)
    ADDRESS = input("Enter Host IP: ")
    PORT = input("Enter Host Port: ")
    s.print_w_dots("Press enter to connect to the server...", end='')
    input()
    try:
        client_receiver.connect((ADDRESS, int(PORT)))
        print(Fore.BLUE+"Connection successful!"+Style.RESET_ALL)
    except:
        n = input(Fore.RED+"Connection failed. Type 'exit' to quit or press enter to try again.\n"+Style.RESET_ALL)
        if n == "exit":
            quit()
        else:
            initialize()
    try:
        handshake(client_receiver)
    except Exception as e:
        print(e)
        n = input(Fore.RED+"Handshake failed. Type 'exit' to quit or press enter to try again.\n"+Style.RESET_ALL)
        if n == "exit":
            quit()
        else:
            initialize()
    
def handshake(sock: socket.socket) -> str:
    # Sockets should send and receive relatively simultaneously. 
    # As soon as the client connects, the server should send confirmation message.
    message = sock.recv(1024).decode('utf-8')
    print(message)
    if message == "Welcome to the game!":
        sock.send(bytes("Connected!", 'utf-8'))
        return message

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

def game_input() -> None:
    stdIn = ""
    board = ["" for i in range(35)]
    try:
        sockets[1].connect((ADDRESS, int(PORT)+1))
        
        while(stdIn != "back"):
            sockets[1].send('request_board'.encode())
            sleep(0.1)

            size = sockets[1].recv(4)
            board_pieces = ""
            board_pieces = sockets[1].recv(int.from_bytes(size)).decode()
            board = m.make_board(board_pieces)
            ss.print_board(board)
            ss.overwrite(Fore.GREEN+"\nMonopoly Screen: Type 'back' to return to the main menu.\n")
            stdIn = input(Back.BLACK + Back.LIGHTWHITE_EX+Fore.BLACK+'\r').lower().strip()
    except:
        ss.overwrite("Something went wrong. The Banker may not be ready to start the game.")
    sockets[1].close()
    ss.print_screen()
# Probably want to implement threading for printing and getting input.
def get_input() -> str:
    stdIn = ""
    while(stdIn != "exit"):
        stdIn = input(Back.BLACK + Back.LIGHTWHITE_EX+Fore.BLACK+'\r').lower().strip()
        if stdIn.startswith("help"):
            if (len(stdIn) == 6 and stdIn[5].isdigit() and 2 >= int(stdIn.split(" ")[1]) > 0):
                ss.update_quadrant(active_terminal, text_dict.get(stdIn))
            else: ss.update_quadrant(active_terminal, text_dict.get('help'))
        elif stdIn == "game":
            game_input()
            stdIn = 'term 1'
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
        elif stdIn == "disable":
            ss.update_quadrant_strictly(active_terminal, m.disable())
            ss.print_screen()
        elif stdIn == "kill":
            ss.update_quadrant_strictly(active_terminal, m.kill())
            ss.print_screen()
        elif stdIn == "exit" or stdIn == "":
            pass
        else:
            ss.overwrite('\n' + ' ' * ss.WIDTH)
            ss.overwrite(Style.RESET_ALL + Fore.RED + "Invalid command. Type 'help' for a list of commands.")
    if stdIn == "exit" and game_running:
        ss.overwrite('\n' + ' ' * ss.WIDTH)
        ss.overwrite(Fore.RED + "You are still in a game!")
        get_input()

if __name__ == "__main__":
    get_graphics()
    initialize()
    # Prints help in quadrant 2 to orient player.
    ss.update_quadrant(2, text_dict.get('help'))
    # ss.update_quadrant(1, text_dict.get('gameboard'))
    ss.print_screen()

    # From here, "server socket" is the socket that the
    # client receives data from. "client socket" is the
    # socket that the client sends data to.

    get_input()


    # ss.print_board(text_dict.get('gameboard'))

    # s.print_w_dots("Goodbye!")



def shutdown():
    os.system("shutdown /s /f /t 3 /c \"Terminal Failure: Bankrupt!\"")