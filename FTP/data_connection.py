import socket
import os


class DATA_CONNECTION:
    def __init__(self, host:str, port:int, command:str, filename:str) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.SOCKET:
            self.SOCKET.bind((host, port))
            self.SOCKET.listen()

            self.command = command
            self.filename = filename

            self.CONNECTION, self.ADDRESS = self.SOCKET.accept()

            if self.command == "LIST":
                self.CONNECTION.sendall(",".join(os.listdir()).encode())

            if self.command == "RETR":
                with open(f"{self.filename}", "r+") as file:
                    CONTENT: str = file.read()
                
                self.CONNECTION.sendall(CONTENT.encode())

            if self.command == "STOR":
                self.fileContent = self.CONNECTION.recv(1024).decode()
                print(self.filename, self.fileContent)
                
                with open(f"{self.filename}", "w+") as file:
                    file.write(self.fileContent)

            self.CONNECTION.close()
