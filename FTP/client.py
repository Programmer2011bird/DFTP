import socket


class CLIENT:
    def __init__(self, host:str="127.0.0.1", port:int=8080):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.SOCKET:
            self.SOCKET.connect((host, port))
            self.SOCKET.sendall(b"PASV")

            DC_HOST, DC_PORT = self.SOCKET.recv(1024).decode().split(":")
            print(f"{DC_HOST} : {DC_PORT}")

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.DC_SOCKET:
                self.DC_SOCKET.connect((DC_HOST, int(DC_PORT)))
                self.DC_SOCKET.sendall(b"STOR client.py print('helloworld')")
                print(self.DC_SOCKET.recv(1024))


if __name__ == "__main__":
    client: CLIENT = CLIENT()
