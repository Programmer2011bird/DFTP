import sha256_calculator
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
                
                SHA256_hash: str = sha256_calculator.calculate_sha256(CONTENT)
                self.CONNECTION.sendall(CONTENT.encode() + b"\r\n||" + SHA256_hash.encode())

            if self.command == "STOR":
                self.fullMessage: bytes = self.CONNECTION.recv(1024)
                self.fileContent, self.RECIEVED_SHA256_HASH = self.fullMessage.split(b"\r\n||")

                self.CALCULATED_SHA256_HASH: str = sha256_calculator.calculate_sha256(str(self.fileContent.decode()))

                if self.CALCULATED_SHA256_HASH == self.RECIEVED_SHA256_HASH.decode():
                    with open(f"{self.filename}", "w+") as file:
                        file.write(self.fileContent.decode())

                    print("✅ File Integrity Verified !")

                elif self.CALCULATED_SHA256_HASH != self.RECIEVED_SHA256_HASH.decode():
                    print("❌ File Integrity Failed !")

            self.CONNECTION.close() 
