import socket
import threading
import os
import style as s

def initialize_terminal():
    os.system("cls")
    print("Welcome to Terminal Monopoly, Banker!")

def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = socket.gethostname()

    # Choose a port that is free
    port = input("Choose a port, such as 3131: ")

    # Bind to the port
    server_socket.bind((host, int(port)))
    s.print_w_dots("Server started on port %s" % port)
    server_socket.listen()
    s.print_w_dots("Waiting for clients...")

    while True:
        # Establish a connection
        client_socket, addr = server_socket.accept()
        print("Got a connection from %s" % str(addr))

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

        # Close the connection
        client_socket.close()

def handle_client(client_socket):
    # Handle communication with the client
    client_socket.send("Welcome to the game!".encode('utf-8'))

    # request = client_socket.recv(1024)
    # print(f"Received: {request.decode('utf-8')}")
    # client_socket.close() # Eventually close the connection

if __name__ == "__main__":
    initialize_terminal()
    start_server()