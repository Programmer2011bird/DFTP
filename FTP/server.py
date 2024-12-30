import data_connection
import threading
import socket


class SERVER:
    def __init__(self, host:str="127.0.0.1", port:int=8080):
        self.DATA_CONNECTION_HOST: str = "127.0.0.1"
        self.DATA_CONNECTION_PORT: int = 2020
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.SOCKET:
            self.SOCKET.bind((host, port))
            self.SOCKET.listen()
            
            while True:
                self.CONNECTION, self.ADDRESS = self.SOCKET.accept()
                
                command, filename = self.CONNECTION.recv(1024).decode().split(" ")

                data_connection_thread = threading.Thread(target=self.connect_data_connection, args=(command, filename))
                data_connection_thread.start()

                self.CONNECTION.sendall(f"{self.DATA_CONNECTION_HOST}:{self.DATA_CONNECTION_PORT}".encode())
                self.CONNECTION.close()

    def connect_data_connection(self, command: str, fileName: str):
        DATA_CONNECTION_HOST: str = "127.0.0.1"
        DATA_CONNECTION_PORT: int = 2020
        DC = data_connection.DATA_CONNECTION(DATA_CONNECTION_HOST, DATA_CONNECTION_PORT, command, fileName)


if __name__ == "__main__":
    server_thread = threading.Thread(target= SERVER)
    server_thread.start()
