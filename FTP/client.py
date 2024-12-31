import sha256_calculator
import socket


class CLIENT:
    def __init__(self, host:str="127.0.0.1", port:int=8080, COMMAND:str=""):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.SOCKET:
            self.SOCKET.connect((host, port))
            self.SOCKET.sendall(COMMAND.encode())

            DC_HOST, DC_PORT = self.SOCKET.recv(1024).decode().split(":")
            print(f"{DC_HOST} : {DC_PORT}")
            
            self.command = COMMAND.split(" ")[0]
            self.fileName = COMMAND.split(" ")[1]
            
            if self.command == "STOR":
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.DC_SOCKET:
                    self.DC_SOCKET.connect((DC_HOST, int(DC_PORT)))
                    
                    with open(f"{self.fileName}", "r+") as file:
                        fileContent: str = file.read()

                    sha256_hash: str = sha256_calculator.calculate_sha256(fileContent)
                    self.fullMessage: bytes = fileContent.encode() + b"\r\n||" + sha256_hash.encode()

                    self.DC_SOCKET.sendall(self.fullMessage)

            elif self.command == "RETR":
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.DC_SOCKET:
                    self.DC_SOCKET.connect((DC_HOST, int(DC_PORT)))
                    
                    self.fullMessage: bytes = self.DC_SOCKET.recv(1024)
                    
                    self.fileContent, self.RECIEVED_SHA256_HASH = self.fullMessage.split(b"\r\n||")
                    self.CALCULATED_SHA256_HASH: str = sha256_calculator.calculate_sha256(str(self.fileContent.decode()))

                    if self.RECIEVED_SHA256_HASH.decode() == self.CALCULATED_SHA256_HASH:
                        print("✅ File Integrity Verified !")

                    elif self.RECIEVED_SHA256_HASH.decode() != self.CALCULATED_SHA256_HASH:
                        print("❌ File Integrity Failed !")

            else:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.DC_SOCKET:
                    self.DC_SOCKET.connect((DC_HOST, int(DC_PORT)))
                    print(self.DC_SOCKET.recv(1024))


if __name__ == "__main__":
    client: CLIENT = CLIENT(COMMAND="STOR ./test.txt")
