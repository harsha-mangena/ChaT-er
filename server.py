import socket
import threading
import structlog

class Server:
    def __init__(self) -> None:
        """
        Initializes the class instance with default values for variables `host`,
        `port`, `server`, `DISCONNECTED`, `clients`, and `nicknames`.

        Args:
            self: An instance of the class.

        Returns:
            None
        """
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 5051
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.DISCONNETED = ['q', 'exit', 'close', 'disconnect']
        self.clients = []
        self.nicknames = []
        self.logger = structlog.get_logger()
    
    def broadcast(self, msg, client=None) -> None:
        """
        Sends a message to all clients in the chatroom except for the client who sent the message.

        :param msg: The message to send to all clients.
        :type msg: str
        :param client: The client who sent the message. This client will not receive the message.
        :type client: Any
        :return: None
        :rtype: None
        """
        for _client in self.clients:
            if _client != client:
                _client.send(msg)
            
    def start_server(self):
        """
        Starts a server by binding to the host and port specified in the instance variables, 
        listening for incoming client connections, and calling the listen function to handle 
        incoming requests. 

        Parameters:
        self (object): The instance of the class that this method operates on.

        Returns:
        None
        """
        self.server.bind((self.host, self.port))
        self.server.listen()
        
        self.logger.info(f'Server is listening on {self.host}:{self.port}')
        
        self.listen()
            
    def handle_client(self, client, addr):
        """
        Handle a client connection by receiving messages from the client and broadcasting them to all other clients.
        
        Args:
            client (socket): The connected socket object representing the client.
            addr (tuple): A tuple containing the IP address and port number of the client.
        
        Returns:
            None
        """
        is_connected = True
        while is_connected:
            try:
                msg = client.recv(1024)
                
                if msg in self.DISCONNETED:
                    is_connected = False
                    break
                
                self.broadcast(msg, client)
                self.logger.info("Total Connections : {}".format(threading.activeCount()-1))
                
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast('{} left!'.format(nickname).encode('ascii'), client)
                self.nicknames.remove(nickname)
                break
    
    def listen(self):
        """
        Listens for incoming connections and accepts them. Once a connection is made, it receives the nickname
        of the user and adds it to the list of nicknames and clients. Then it broadcasts to all users that the
        new user has joined. Finally, it starts a new thread to handle the client and its messages.

        Parameters:
        None

        Returns:
        None
        """
        while True:
            client, addr = self.server.accept()
            
            client.send('GET_NAME'.encode('ascii'))
            self.nickname = client.recv(1024).decode('ascii')
            self.nicknames.append(self.nickname)
            self.clients.append(client)
            
        
            self.logger.info("Welcome {} to the chatroom".format(self.nickname))
            self.broadcast("{} joined!".format(self.nickname).encode('ascii'), client)
            client.send("{} connected to server!".format(self.nickname).encode('ascii'))

            # Start Handling Thread For Client
            self.logger.info("Starting thread for {}".format(self.nickname))
            threading.Thread(target=self.handle_client, args=(client, addr)).start()
        
