import socket


class DATA_CONNECTION:
    def __init__(self, host:str, port:int) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.SOCKET:
            self.SOCKET.bind((host, port))
            self.SOCKET.listen()

            self.CONNECTION, self.ADDRESS = self.SOCKET.accept()
            print("data connection:", self.CONNECTION.recv(1024).decode())
            self.CONNECTION.sendall(b"hello ! I'm A Data Connection !")

            self.CONNECTION.close()

class SERVER:
    def __init__(self, host:str="127.0.0.1", port:int=8080):
        self.DATA_CONNECTION_HOST: str = "127.0.0.1"
        self.DATA_CONNECTION_PORT: int = 2020
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.SOCKET:
            self.SOCKET.bind((host, port))
            self.SOCKET.listen()

            self.CONNECTION, self.ADDRESS = self.SOCKET.accept()
            print("server:", self.CONNECTION.recv(1024).decode())
            self.CONNECTION.sendall(f"{self.DATA_CONNECTION_HOST}:{self.DATA_CONNECTION_PORT}".encode())

            self.CONNECTION.close()


if __name__ == "__main__":
    server: SERVER = SERVER()
