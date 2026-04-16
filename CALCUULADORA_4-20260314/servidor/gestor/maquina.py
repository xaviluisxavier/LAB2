import socket
import json
from servidor.operacoes.somar import Somar
from servidor.operacoes.subtrair import Subtrair
from servidor.operacoes.dividir import Dividir

COMMAND_SIZE = 9
INT_SIZE = 8
OBJ_OP = "add_obj  "
BYE_OP = "bye      "
END_OP = "stop     "

class Maquina:
    """
    Recebe os pedidos via rede (Sockets), processa a informação JSON, 
    chama a operação matemática correspondente e devolve o resultado.
    """
    def __init__(self):
        self.sum = Somar()
        self.sub = Subtrair()
        self.div = Dividir()

    def receive_int(self, connection):
        data = connection.recv(INT_SIZE)
        return int.from_bytes(data, byteorder='big', signed=True)

    def receive_object(self, connection):
        size = self.receive_int(connection)
        data = connection.recv(size)
        return json.loads(data.decode('utf-8'))

    def execute(self):
        """Substituição do execute pelo código do server_math_ver_3 """
        s = socket.socket()
        s.bind(('', 35000))
        s.listen(1)
        print("Servidor aguardando ligações na porta 35000.")
        
        keep_running = True
        while keep_running:
            connection, address = s.accept()
            last_request = False
            while not last_request:
                request_type = connection.recv(COMMAND_SIZE).decode()
                
                if request_type == OBJ_OP:
                    obj = self.receive_object(connection)
                    oper = obj.get("oper")
                    op1 = obj.get("op1")
                    op2 = obj.get("op2")
                    
                    if oper == "+": res = self.sum.execute(op1, op2)
                    elif oper == "-": res = self.sub.execute(op1, op2)
                    elif oper == "/": 
                        self.div.x, self.div.y = op1, op2
                        res = self.div.execute()
                    
                    connection.send(int(res).to_bytes(INT_SIZE, byteorder="big", signed=True))
                
                elif request_type == BYE_OP:
                    last_request = True
                elif request_type == END_OP:
                    last_request = True
                    keep_running = False
            connection.close()
        s.close()
