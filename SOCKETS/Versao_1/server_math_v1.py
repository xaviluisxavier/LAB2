import socket

PORT = 35000
SERVER_ADDRESS = "localhost"
INT_SIZE = 8
COMMAND_SIZE = 4

# interaction with sockets
def receive_int(connection, n_bytes: int) -> int:
    data = connection.recv(n_bytes)
    return int.from_bytes(data, byteorder='big', signed=True)

def send_int(connection, value: int, n_bytes: int) -> None:
    connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

def receive_str(connection, n_bytes: int) -> str:
    data = connection.recv(n_bytes)
    return data.decode()

def send_str(connection, value: str) -> None:
    connection.send(value.encode())

def main():
    s = socket.socket()
    s.bind(('', PORT))
    s.listen(1)
    print("Waiting for clients to connect on port " + str(PORT))
    keep_running = True
    while keep_running:
        connection, address = s.accept()
        print("Client " + str(address) + " just connected")
        last_request = False
        while not last_request:
            request_type = receive_str(connection, COMMAND_SIZE)
            if request_type == "_add":
                a = receive_int(connection, INT_SIZE)
                b = receive_int(connection, INT_SIZE)
                print("Pediram para somar:", a, "+", b)
                result = a + b
                send_int(connection, result, INT_SIZE)
            elif request_type == "_sub":
                a = receive_int(connection, INT_SIZE)
                b = receive_int(connection, INT_SIZE)
                print("Pediram para subtrair:", a, "-", b)
                result = a - b
                send_int(connection, result, INT_SIZE)
            elif request_type == "_bye":
                last_request = True
                keep_running = False
                s.close()
    print("Server stopped")

if __name__ == "__main__":
    main()
