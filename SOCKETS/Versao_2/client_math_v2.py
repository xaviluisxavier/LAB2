import socket

COMMAND_SIZE = 9
INT_SIZE = 8
ADD_OP = "add      "
OBJ_OP = "add_obj  "
SYM_OP = "sym      "
BYE_OP = "bye      "
SUB_OP = "sub      "
END_OP = "stop     "
PORT = 35000
SERVER_ADDRESS = "localhost"

# ----- enviar e receber strings ----- #
def receive_str(connect, n_bytes: int) -> str:
    """
    :param n_bytes: The number of bytes to read from the current connection
    :return: The next string read from the current connection
    """
    data = connect.recv(n_bytes)
    return data.decode()

def send_str(connect, value: str) -> None:
    connect.send(value.encode())

def send_int(connect: socket.socket, value: int, n_bytes: int) -> None:
    connect.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

def receive_int(connect: socket.socket, n_bytes: int) -> int:
    data = connect.recv(n_bytes)
    return int.from_bytes(data, byteorder='big', signed=True)


def main():
    # Socket & ligação
    connection = socket.socket()
    connection.connect((SERVER_ADDRESS, PORT))

    # Testar a operação de soma
    a = 10
    b = 15
    send_str(connection, ADD_OP)
    send_int(connection, a, INT_SIZE)
    send_int(connection, b, INT_SIZE)
    res = receive_int(connection, INT_SIZE)
    print("O resultado da soma é:", res)

    # Testar duas operações de subtração
    for i in range(2):
        a += 1
        send_str(connection, SUB_OP)
        send_int(connection, a, INT_SIZE)
        send_int(connection, b, INT_SIZE)
        res = receive_int(connection, INT_SIZE)
        print("O resultado da subtração é:", res)

    # Opção 1: Fechar apenas a sessão do cliente (servidor mantém-se ativo)
    #send_str(connection, BYE_OP)
    #print("Connection session closed. Server remains active.")
    #connection.close()

    # Opção 2: Fechar cliente E servidor
    send_str(connection, END_OP)
    print("Server stop requested.")
    connection.close()


if __name__ == "__main__":
    main()