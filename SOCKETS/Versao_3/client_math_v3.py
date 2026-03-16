import socket
import json

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

# ----- enviar e receber primitivos ----- #
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

# ----- enviar e receber objetos (JSON) ----- #
def send_object(connection, obj) -> None:
    """
    Envia um objeto Python (dicionário, lista, etc.) serializado em JSON.
    1º: envia o tamanho em bytes do objeto serializado.
    2º: envia os dados JSON.

    json.dumps() serializa o objeto Python para uma string no formato JSON.
    Codificamos em UTF-8 para transformar em bytes que o socket pode enviar.
    """
    data = json.dumps(obj).encode('utf-8')
    size = len(data)
    send_int(connection, size, INT_SIZE)  # Envio do tamanho
    connection.send(data)                 # Envio do objeto

def receive_object(connection):
    """
    Recebe um objeto Python serializado em JSON.
    1º: lê o tamanho em bytes.
    2º: lê os dados e desserializa.

    json.loads() converte a string JSON de volta a um objeto Python
    (ex: dicionário ou lista), o inverso de json.dumps().
    """
    size = receive_int(connection, INT_SIZE)  # Recebe o tamanho
    data = connection.recv(size)              # Recebe os bytes do objeto
    return json.loads(data.decode('utf-8'))
# -------------------------------------------#


def main():
    # Socket & ligação
    connection = socket.socket()
    connection.connect((SERVER_ADDRESS, PORT))

    # --- Teste 1: Operação de soma simples (ADD_OP) ---
    a = 10
    b = 15
    send_str(connection, ADD_OP)
    send_int(connection, a, INT_SIZE)
    send_int(connection, b, INT_SIZE)
    res = receive_int(connection, INT_SIZE)
    print("O resultado da soma é:", res)

    # --- Teste 2: Operação OBJ_OP com dicionário ---
    # O cliente envia um dicionário com a operação e os operandos.
    # O servidor descodifica, realiza a operação e devolve o resultado como inteiro.
    operacao = {"oper": "+", "op1": 4, "op2": 5}
    send_str(connection, OBJ_OP)
    send_object(connection, operacao)
    res = receive_int(connection, INT_SIZE)
    print(f"OBJ_OP resultado de {operacao}: {res}")

    # Mais exemplos com OBJ_OP
    operacao2 = {"oper": "-", "op1": 20, "op2": 7}
    send_str(connection, OBJ_OP)
    send_object(connection, operacao2)
    res = receive_int(connection, INT_SIZE)
    print(f"OBJ_OP resultado de {operacao2}: {res}")

    # --- Teste 3: Duas operações de subtração simples (SUB_OP) ---
    for i in range(2):
        a += 1
        send_str(connection, SUB_OP)
        send_int(connection, a, INT_SIZE)
        send_int(connection, b, INT_SIZE)
        res = receive_int(connection, INT_SIZE)
        print("O resultado da subtração é:", res)

    # --- Fechar a sessão (servidor mantém-se ativo para novos clientes) ---
    send_str(connection, BYE_OP)
    print("Connection session closed. Server remains active.")
    connection.close()

    # --- Para terminar o servidor também, substituir BYE_OP por END_OP ---
    # send_str(connection, END_OP)
    # print("Server stop requested.")
    # connection.close()


if __name__ == "__main__":
    main()