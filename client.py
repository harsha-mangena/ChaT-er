import socket
import threading

class Client:
    def __init__(self, nickname) -> None:
        """
        Initializes a new instance of the class with the given nickname. Sets the `name` attribute to the given
        nickname. Sets the `host` attribute to the IP address of the current machine. Sets the `port` attribute to
        `5051`. Creates a new TCP/IP socket using the `AF_INET` address family and the `SOCK_STREAM` socket type.
        Connects the socket to the specified address `(host, port)`.

        :param nickname: A string representing the nickname for the new instance.
        :type nickname: str
        :return: None
        """
        self.name = nickname
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 5051
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

    def receive(self):
        """
        A function that receives messages from the server and sends the client's nickname if requested. 
        If an error occurs during message reception, the function will close the connection and exit.

        Parameters:
        - None

        Return:
        - None
        """
        while True:
            try:
                # Receive Message From Server
                # If 'GET_NAME' Send Nickname
                message = self.client.recv(1024).decode('ascii')
                if message == 'GET_NAME':
                    self.client.send(self.name.encode('ascii'))
                else:
                    print(message)
            except:
                # Close Connection When Error
                print("An error occured!")
                self.client.close()
                break  
      
    def write(self):
        """
        Writes the user input to the client indefinitely.

        :param self: The instance of the class.
        :return: None.
        """
        while True:
            message = '{}: {}'.format(self.name, input(''))
            self.client.send(message.encode('ascii'))
            
    def start(self):
        """
        Starts two threads, one for receiving and one for writing, in order to enable 
        concurrent communication between client and server. The function takes no 
        parameters and does not return anything.
        """
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()

name = input('Enter Name:')        
client = Client(name)
client.start()


