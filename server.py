import socket
import threading
import random

IP_ADDR = socket.gethostbyname(socket.gethostname())
PORT = random.randint(0,65300)
ADDR = (IP_ADDR, PORT)
FORMAT = 'utf-8'
DISCONNECT = ['close', 'exit', 'disconnect']

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def start_server():
    print(f'[STARTING] Server is starting on {IP_ADDR}:{PORT}')
    server.listen()
    
    while True:
        conn, addr = server.accept()
        new_connection_thread = threading.Thread(target=handle_client, args=(conn, addr))
        new_connection_thread.start()

def encode_message():
    pass

def decode_message():
    pass 

def handle_client(conn, addr):
    is_connected = True
    while is_connected:
        msg_length = conn.recv(1024).decode(FORMAT)
        msg_length = int(msg_length)
        
        if msg_length:
            msg = conn.recv(msg_length).decode(FORMAT)
            
            if msg in DISCONNECT:
                is_connected = False
            
            print(f'{addr} : {msg}')
    
    conn.close()

if __name__ == '__main__':
    start_server()
            