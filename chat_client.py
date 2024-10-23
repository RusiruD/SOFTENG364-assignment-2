import select
import socket
import sys
import signal
import ssl
import os
import maskpass
import argparse
import threading
import bcrypt
import warnings

from userDetailsManager import userDetailsManager
from utils import send, receive  # Assuming these are implemented in utils
from counterManager import increment_counter, get_counter, decrement_counter

# Create a userDetailsManager instance and load the userDetails array
userDetails = userDetailsManager()
userDetails.load_array()

# Initialize variables and ignore Deprecation warnings
SERVER_HOST = 'localhost'
chatname = ''
stop_thread = False
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Send data to the server
def get_and_send(client, name):
    
    while not stop_thread:
        data = sys.stdin.readline().strip()
        if data == 'Q':
            print("Logging out and leaving the chat room")
            # Logout the user 
            userDetails.set_login(name, 0)
            # Decrement amount of clients
            exit()
        if data:
            send(client.sock, data)  # Send the message to the server

def exit():
   decrement_counter(0)
   os._exit(0)

class ChatClient:
    
    # A command line chat client using select
    def __init__(self, name, port, host=SERVER_HOST):
       

        global chatname
        alive = True
        if get_counter(0) >= 2:
           
            print("Maximum number of clients reached")
            sys.exit(1)

        increment_counter(0)
        print("Welcome to the chat room")
        
       
        if(userDetails.get_array_size() == 0):
           print("Would you like to Register or Quit?, type 'R' for Register or 'Q' for Quit")
        else:
           print("Would you like to Login, Register or Quit?, type 'L' for Login, 'R' for Register or 'Q' for Quit")
        
        choice = input("Choice: ")
        print("Type 'Q' in both username and password to quit and leave the chat room")


        # Continuously ask for the choice until the user types 'L' or 'R'
        if userDetails.get_array_size() == 0:
            # Only allow 'R' or 'E' if the array size is 0
            while choice != 'R' and choice != 'Q':
                print("Invalid choice, please type 'R' for Register or 'Q' for Quit")
                choice = input("Choice: ")
                print("Type 'Q' in both username and password to quit and leave the chat room")

        else:
            # Allow 'L', 'R', or 'E' for non-zero array size
            while choice != 'L' and choice != 'R' and choice != 'Q':
                print("Invalid choice, please type 'L' for Login, 'R' for Register, or 'Q' for Quit")
                choice = input("Choice: ")
                print("Type 'Q' in both username and password to quit and leave the chat room")
            

        # Allow the user to input a username and a password
        if choice == 'L' and userDetails.get_array_size() != 0:
            print("Login")
            while True:
                username = input('Username: ')
                password = maskpass.advpass(prompt='Password (Left Ctrl to reveal): ')
                password_bytes = password.encode('utf-8')  # Convert string to bytes

                if(username == 'Q' and password == 'Q'):
                    print("Exiting chat room")
                    exit()

                # Check if the user is already logged in
                if userDetails.is_logged_in(username) == 1:
                    print("You are already logged in. Please log in with a different account.")
                    continue  # Prompt for a different username

                # Check if the user exists
                if not userDetails.find_user(username, password_bytes):
                    print("Username or Password are incorrect.")
                    continue  # Prompt for username and password again

                if userDetails.find_user(username, password_bytes):
                    print("Logged in Successfully, type 'Q' to log out and leave the chat room")
                    userDetails.set_login(username, 1)
                    chatname = username
                    break
                
        # Allow the user to input a username and a password and register for the service
        elif choice == 'R':
            print("Register")
            username = input('Username: ')

            # Check if the username already exists, if it does ask the user to input a different username
            while userDetails.find_username(username):
                print("Username already exists")
                username = input('Username: ')
            if(username == 'Q' and password == 'Q'):
                print("Exiting chat room")
                exit()
            # Allow user to input a password and hash it using bcrypt and add it to the userDetails array
            password = maskpass.advpass(prompt='Password (Left Ctrl to reveal): ')
            password_bytes = password.encode('utf-8')  # Convert string to bytes
            hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
            loggedin = 1
            userDetails.add_user(username, hashed_password, loggedin)
            print("Registered Successfully, you are now logged in, type 'Q' to log out and leave the chat room")
            chatname = username
        elif choice == 'Q':
            print("Exiting chat room")
            exit()
       

        # Set chat_client variables
        self.name = chatname
        self.connected = False
        self.host = host
        self.port = port
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.set_ciphers('AES128-SHA')
        
        # Initial prompt
        self.prompt = f'[{name}@{socket.gethostname()}]> '
       
        # Connect to server at port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock = self.context.wrap_socket(self.sock, server_hostname=host)
            self.sock.connect((host, self.port))
            self.connected = True
            
            # Send my name...
            send(self.sock, 'NAME: ' + self.name)
            data = receive(self.sock)
            self.prompt = 'me: '
           
            threading.Thread(target=get_and_send, args=(self, chatname)).start()  # Start the thread

        except socket.error as e:
            print(f'Failed to connect to chat server @ port {self.port}')
            sys.exit(1)

    def cleanup(self):
        """Close the connection and wait for the thread to terminate."""
        self.sock.close()

    def run(self):
        global stop_thread
        """Chat client main loop"""
        while self.connected:
            try:
                sys.stdout.write(self.prompt)
                sys.stdout.flush()

                # Wait for input from stdin and socket
                readable, writeable, exceptional = select.select([self.sock], [], [])

                for sock in readable:
                    if sock == self.sock:
                        data = receive(self.sock)
                    

                        if get_counter(1) == 0:
                                sys.stdout.write('\n' + data + '\n')
                                sys.stdout.flush()
                                increment_counter(1)
                        else:
                                sys.stdout.write(data + '\n')
                                sys.stdout.flush()

            except KeyboardInterrupt:
                print("Client interrupted.")
                stop_thread = True  # Signal to stop the input thread
                self.cleanup()
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', action="store", dest="name", required=True)
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args()

    port = given_args.port
    name = given_args.name

    client = ChatClient(name=name, port=port)
    client.run()
