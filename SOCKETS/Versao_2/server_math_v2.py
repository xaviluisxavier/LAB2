import socket

COMMAND_SIZE = 9
INT_SIZE = 8
ADD_OP = "add      "
OBJ_OP = "add_obj  "
SYM_OP = "sym      "
SUB_OP = "sub      "
BYE_OP = "bye      "
END_OP = "stop     "
PORT = 35000
SERVER_ADDRESS = "localhost"

# ---------------------- interaction with sockets ------------------------------
def receive_int(connection, n_bytes: int) -> int:
    """
    :param n_bytes: The number of bytes to read from the current connection
    :return: The next integer read from the current connection
    """
    data = connection.recv(n_bytes)
    return int.from_bytes(data, byteorder='big', signed=True)

def send_int(connection, value: int, n_bytes: int) -> None:
    """
    :param value: The integer value to be sent to the current connection
    :param n_bytes: The number of bytes to send
    """
    connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

def receive_str(connection, n_bytes: int) -> str:
    """
    :param n_bytes: The number of bytes to read from the current connection
    :return: The next string read from the current connection
    """
    data = connection.recv(n_bytes)
    return data.decode()

def send_str(connection, value: str) -> None:
    """
    :param value: The string value to send to the current connection
    """
    # BUG ORIGINAL: connection.connection.send(value.encode())
    connection.send(value.encode())
# ---------------------------------------------------------------------------------------


def main():
    """
    Runs the server until the client sends a "terminate" action
    """
    s = socket.socket()
    s.bind(('', PORT))
    s.listen(1)
    print("Waiting for clients to connect on port " + str(PORT))
    keep_running = True
    while keep_running:
        print("On accept...")
        connection, address = s.accept()
        print("Client " + str(address) + " just connected")
        last_request = False
        while not last_request:
            request_type = receive_str(connection, COMMAND_SIZE)
            if request_type == ADD_OP:
                a = receive_int(connection, INT_SIZE)
                b = receive_int(connection, INT_SIZE)
                print("Pediram para somar:", a, "+", b)
                result = a + b
                send_int(connection, result, INT_SIZE)
            elif request_type == SUB_OP:
                a = receive_int(connection, INT_SIZE)
                b = receive_int(connection, INT_SIZE)
                print("Pediram para subtrair:", a, "-", b)
                result = a - b
                send_int(connection, result, INT_SIZE)
            elif request_type == BYE_OP:
                # O cliente termina a sua sessão mas o servidor mantém-se ativo
                # para aceitar novos clientes
                print("Client disconnected. Waiting for new connections...")
                last_request = True
            elif request_type == END_OP:
                # O cliente pede ao servidor para também terminar
                print("Server stop requested by client.")
                last_request = True
                keep_running = False
    print("Stopping...")
    s.close()
    print("Server stopped")

if __name__ == "__main__":
    main()