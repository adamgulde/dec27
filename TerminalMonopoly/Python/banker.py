import socket
import threading
import os
import style as s
import screenspace as ss
import socket
import select
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
    num_players = 1
    handshakes = [False] * num_players

    # start_receiver(handshakes)
    game_full = False
    while not game_full:
        # Accepts connections while there are less than <num_players> players
        sleep(1)
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

def start_receiver(transmitter_socket: socket.socket):
    global player_data
    s.print_w_dots('[RECEIVER] Receiver started!') 
    # https://stackoverflow.com/a/43151772/19535084
    with socket.socket() as server:
        host = socket.gethostname()
        ip_address = socket.gethostbyname(host)
        server.bind((ip_address,int(transmitter_socket.getsockname()[1]+1)))
        server.listen()
        s.print_w_dots('[RECEIVER] Receiver accepting connections at {}'.format(port+1))
        to_read = [server]  # add server to list of readable sockets.
        players = {}
        while True:
            # check for a connection to the server or data ready from clients.
            # readers will be empty on timeout.
            readers,_,_ = select.select(to_read,[],[],0.5)
            for reader in readers:
                if reader is server:
                    player,address = reader.accept()
                    print('connected',address)
                    players[player] = address # store address of client in dict
                    to_read.append(player) # add client to list of readable sockets
                else:
                    # Simplified, really need a message protocol here.
                    # For example, could receive a partial UTF-8 encoded sequence.
                    data = reader.recv(1024)
                    print('received: {}'.format(data), end='')
                    if data.decode() == 'request_board':
                        # Player requests board:
                        # Send board size, then board
                        board = s.get_graphics()['gameboard']
                        size = len(board.encode())
                        reader.send(size.to_bytes(4,byteorder='big'))
                        sleep(0.1)
                        reader.send(board.encode())
                    if not data: # No data indicates disconnect
                        print('disconnected',players[reader])
                        to_read.remove(reader) # remove from monitoring
                        del players[reader] # remove from dict as well
                    else:
                        print(players[reader],data.decode())
            print('.',flush=True,end='')
    s.print_w_dots('[RECEIVER] Receiver stopped.')


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
    start_receiver(server_socket)
    print(f"Found {players}, each at: ")
    for player in player_data:
        print(s.Fore.BLUE+ str(player_data[player][socket.socket]))
    print(s.Style.RESET_ALL)
    set_gamerules()
