import socket
import json

COMMAND_SIZE = 9
INT_SIZE = 8
OBJ_OP = "add_obj  "
BYE_OP = "bye      "

class Interacao:
    def send_object(self, connection, obj):
        data = json.dumps(obj).encode('utf-8')
        size = len(data)
        connection.send(size.to_bytes(INT_SIZE, byteorder="big", signed=True))
        connection.send(data)

    def execute(self):
        """Substituição do execute pelo código do client_math_ver_3 """
        print("Operação (+, -, /):")
        op = input().strip()
        x = int(input("x: "))
        y = int(input("y: "))

        conn = socket.socket()
        conn.connect(("localhost", 35000))

        # Enviar OBJ_OP e o dicionário 
        conn.send(OBJ_OP.encode())
        self.send_object(conn, {"oper": op, "op1": x, "op2": y})

        # Receber resultado
        res_data = conn.recv(INT_SIZE)
        res = int.from_bytes(res_data, byteorder='big', signed=True)
        print(f"Resultado: {res}")

        conn.send(BYE_OP.encode())
        conn.close()