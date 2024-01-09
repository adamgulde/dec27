import os
import socket
from colorama import Fore, Style
import style as s


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
    communicate(client_socket)

def communicate(sock: socket.socket) -> None:
    message = sock.recv(1024).decode('ascii')
    if message == "exit":
        sock.close()
        quit()
    print(message)

if __name__ == "__main__":
    initialize()
    s.print_w_dots("Goodbye!")