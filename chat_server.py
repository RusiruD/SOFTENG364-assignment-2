import select
import socket
import sys
import signal
import argparse
import ssl
import warnings
from utils import *
from counterManager import create_counter_file, reset_counter,decrement_counter

SERVER_HOST = 'localhost'
create_counter_file()
reset_counter()
warnings.filterwarnings("ignore", category=DeprecationWarning)

class ChatServer(object):
    """ An example chat server using select """
    def __init__(self, port, backlog=5):
      
        self.last_client = None
        self.clients = 0
        self.clientmap = {}
        self.outputs = []  # list output sockets

        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.load_cert_chain(certfile="cert.pem", keyfile="cert.pem")
        self.context.load_verify_locations('cert.pem')
        self.context.set_ciphers('AES128-SHA')

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, port))
        self.server.listen(backlog)
        self.server = self.context.wrap_socket(self.server, server_side=True)

        # Catch keyboard interrupts
        signal.signal(signal.SIGINT, self.sighandler)

        print(f'Server listening to port: {port} ...')

    def sighandler(self, signum, frame):
        # Clean up client outputs
        print('Shutting down server...')

        # Close existing client sockets
        for output in self.outputs:
            output.close()

        self.server.close()

    def get_client_name(self, client):
       # Return the name of the client 
    
        info = self.clientmap[client]
        host, name = info[0][0], info[1]
        
       
        return (name)
 
    
    def run(self):
      
        inputs = [self.server]
        self.outputs = []
        running = True
        while running:
            try:
                readable, writeable, exceptional = select.select(
                    inputs, self.outputs, [])
            except select.error as e:
                break

            for sock in readable:
                sys.stdout.flush()
                if sock == self.server:
                   
                    # handle the server socket
                    if self.clients < 2:
                        client, address = self.server.accept()
                        print(
                            f'Chat server: got connection {client.fileno()} from {address}')
                        
                        # Read the login name
                        cname = receive(client).split('NAME: ')[1]
                        print(cname + ' has joined the chat')

                        # Compute client name and send back
                        self.clients += 1

                        send(client, f'CLIENT: {str(address[0])}')
                        inputs.append(client)

                        self.clientmap[client] = (address, cname)
                        # Send joining information to other clients
                        msg = f'(Connected: New client ({self.clients}) from {self.get_client_name(client)})'
                        decrement_counter(1)
                        
                        self.outputs.append(client)

              
                else:
                    # handle all other sockets
                    try:
                        data = receive(sock)
                        if data:
                            if(sock==self.last_client):
                                decrement_counter(1)
                            # Send as new client's message...
                            msg = f'{self.get_client_name(sock)}: {data}'
                          
                            # Send data to all except ourself
                            for output in self.outputs:
                                if output != sock:
                                    send(output, msg)
                            self.last_client=sock
                        else:
                            print(f'Chat server: {sock.fileno()} hung up')
                            self.clients -= 1
                            sock.close()
                            inputs.remove(sock)
                            self.outputs.remove(sock)
                            #reset message counter
                       
                            # Sending client leaving information to others
                            msg = f'\n(Now hung up: Client from {self.get_client_name(sock)})'
                           

                          
                           


                            for output in self.outputs:
                                send(output, msg)
                    except socket.error as e:
                        # Remove
                        inputs.remove(sock)
                        self.outputs.remove(sock)
                

        self.server.close()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Socket Server Example with Select')
    parser.add_argument('--name', action="store", dest="name", required=True)
    parser.add_argument('--port', action="store",
                        dest="port", type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    name = given_args.name

    server = ChatServer(port)
    server.run()
