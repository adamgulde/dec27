import socket
import threading
import os
import style as s
import socket
from time import sleep

bank_cash = 100000
starting_cash = 1500
players = 0
port = 3131
player_data = {1: {
                    socket.socket: "",
                    "name": "",
                    "money": starting_cash,
                    "properties": []

                }, 2: {
                    socket.socket: "",
                    "name": "",
                    "money": starting_cash,
                    "properties": []    

                }, 3: {
                    socket.socket: "",
                    "name": "",
                    "money": starting_cash,
                    "properties": []

                }, 4: {
                    socket.socket: "",
                    "name": "",
                    "money": starting_cash,
                    "properties": []

                }}

def initialize_terminal():
    os.system("cls")
    print("Welcome to Terminal Monopoly, Banker!")

def start_server() -> socket.socket:
    global players
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = socket.gethostname()
    ip_address = socket.gethostbyname(host)

    # Choose a port that is free
    port = int(input("Choose a port, such as 3131: "))

    # Bind to the port
    # server_socket.bind(('localhost', port))
    server_socket.bind((host, port))
    s.print_w_dots("Server started on %s port %s" % (ip_address, port))
    server_socket.listen()

    s.print_w_dots("Waiting for clients...")
    
    # TEMP VARIABLE: Players should be hardcoded to 4 for printing/playing purposes
    num_players = 2
    handshakes = [False] * num_players

    # start_receiver(handshakes)
    game_full = False
    while not game_full:
        # Accepts connections while there are less than <num_players> players
        sleep(2)
        if players != num_players:
            client_socket, addr = server_socket.accept()
            print("Got a connection from %s" % str(addr))
            client_handler = threading.Thread(target=handshake, args=(client_socket,handshakes))
            client_handler.start()
        else: 
            game_full = True
            # # Give program a moment to evaluate handshakes
            # for h in handshakes:
            #     sleep(1)
            #     if h == False:
            #         players -= 1
            # break
    s.print_w_dots("Game is full. Starting game...")
    s.print_w_dots("")
    s.print_w_dots("")
    s.print_w_dots("")
    return server_socket

def start_receiver(handshakes: []):
    s.print_w_dots('[RECEIVER] Receiver started!') 
    ip_address = socket.gethostbyname(socket.gethostname())
    server_receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_receiver.bind((ip_address, port+1))
    server_receiver.listen()
    s.print_w_dots('[RECEIVER] Receiver accepting connections at {}'.format(port+1))
    while(True):
        data = server_receiver.recv(1000).decode()
        print(f"[RECEIVER THREAD] Received data: {data}")
        if data == "Connected!":
            pass
        if data == "quit":
            break
    server_receiver.close()
    print('[RECEIVER] Receiver stopped.')

def handshake(client_socket: socket.socket, handshakes: []):
    global players, player_data
    # Attempt handshake
    client_socket.send("Welcome to the game!".encode('utf-8'))
    message = client_socket.recv(1024).decode('utf-8')
    if message == "Connected!":
        handshakes[players] = True
        players += 1
        player_data[players][socket.socket] = client_socket
    else: 
        handshakes[players] = False

def update_clients(client_socket: socket.socket):
    pass

def set_gamerules():
    global bank_cash, starting_cash
    bank_cash = input("Enter the amount of money the bank starts with: ")
    starting_cash = input("Enter the amount of money each player starts with: ")

if __name__ == "__main__":
    initialize_terminal()
    server_socket = start_server()
    print(f"Found {players}, each at: ")
    for player in player_data:
        print(s.Fore.BLUE+ str(player_data[player][socket.socket]))
    print(s.Style.RESET_ALL)
    set_gamerules()
