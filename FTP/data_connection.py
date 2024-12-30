import socket
import os


class DATA_CONNECTION:
    def __init__(self, host:str, port:int) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.SOCKET:
            self.SOCKET.bind((host, port))
            self.SOCKET.listen()

            self.CONNECTION, self.ADDRESS = self.SOCKET.accept()
            self.message = self.CONNECTION.recv(1024).decode().split(" ")
            self.command = self.message[0]
            self.filename = self.message[1]

            if self.command == "LIST":
                self.CONNECTION.sendall(",".join(os.listdir()).encode())

            if self.command == "RETR":
                with open(f"{self.filename}", "r+") as file:
                    CONTENT: str = file.read()
                
                self.CONNECTION.sendall(CONTENT.encode())

            if self.command == "STOR":
                print(self.filename, self.message[2])

            self.CONNECTION.close()


if __name__ == "__main__":
    DATA_CONNECTION_HOST: str = "127.0.0.1"
    DATA_CONNECTION_PORT: int = 2020
    DC = DATA_CONNECTION(DATA_CONNECTION_HOST, DATA_CONNECTION_PORT)
