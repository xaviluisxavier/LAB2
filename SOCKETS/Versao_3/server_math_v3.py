import socket
import json

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

#  interaction with sockets 
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
    connection.send(value.encode())

def send_object(connection, obj) -> None:
    """
    Envia um objeto Python (dicionário, lista, etc.) serializado em JSON.
    1º: envia o tamanho em bytes do objeto serializado.
    2º: envia os dados JSON.
    
    json.dumps() converte o objeto Python para uma string JSON.
    Depois codificamos em UTF-8 para obter bytes prontos a enviar pelo socket.
    """
    data = json.dumps(obj).encode('utf-8')
    size = len(data)
    send_int(connection, size, INT_SIZE)  # Envio do tamanho
    connection.send(data)                 # Envio do objeto

def receive_object(connection):
    """
    Recebe um objeto Python (dicionário, lista, etc.) serializado em JSON.
    1º: lê o tamanho em bytes do objeto.
    2º: lê os dados JSON e desserializa-os.
    
    json.loads() converte a string JSON de volta a um objeto Python
    (dicionário, lista, etc.), o inverso de json.dumps().
    """
    size = receive_int(connection, INT_SIZE)  # Recebe o tamanho
    data = connection.recv(size)              # Recebe o objeto
    return json.loads(data.decode('utf-8'))

def main():
    """
    Runs the server until the client sends a "stop" action (END_OP).
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

            elif request_type == OBJ_OP:
                # Recebe o dicionário {"oper": "+", "op1": valor1, "op2": valor2}
                obj = receive_object(connection)
                print("Recebeu objeto:", obj)
                oper = obj.get("oper")
                op1 = obj.get("op1")
                op2 = obj.get("op2")
                if oper == "+":
                    result = op1 + op2
                    print(f"Pediram OBJ_OP soma: {op1} + {op2} = {result}")
                elif oper == "-":
                    result = op1 - op2
                    print(f"Pediram OBJ_OP subtração: {op1} - {op2} = {result}")
                elif oper == "*":
                    result = op1 * op2
                    print(f"Pediram OBJ_OP multiplicação: {op1} * {op2} = {result}")
                elif oper == "/" and op2 != 0:
                    result = op1 / op2
                    print(f"Pediram OBJ_OP divisão: {op1} / {op2} = {result}")
                else:
                    result = 0
                    print("Operação desconhecida ou divisão por zero")
                send_int(connection, int(result), INT_SIZE)

            elif request_type == BYE_OP:
                print("Client disconnected. Waiting for new connections...")
                last_request = True

            elif request_type == END_OP:
                print("Server stop requested by client.")
                last_request = True
                keep_running = False

    print("Stopping...")
    s.close()
    print("Server stopped")

if __name__ == "__main__":
    main()
