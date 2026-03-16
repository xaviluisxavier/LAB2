import socket
import json
from servidor.operacoes.somar import Somar
from servidor.operacoes.dividir import Dividir

INT_SIZE = 4

def receive_int(connection, size):
    """Função auxiliar para receber o tamanho do objeto."""
    data = connection.recv(size)
    if not data: return 0
    return int.from_bytes(data, byteorder='big')

def receive_object(connection):
    """1º: lê tamanho, 2º lê dados."""
    size = receive_int(connection, INT_SIZE)
    if size == 0: return None
    data = connection.recv(size)
    return json.loads(data.decode('utf-8'))

class Maquina:
    def __init__(self):
        self.sum = Somar()
        self.div = Dividir()
        
    def execute_calc(self, op:str, op1:float, op2:float):
        """Lógica original de execução extraída para ser chamada pelo socket."""
        if op == "+":
            res = self.sum.execute(op1, op2)
        elif op == "/":
            self.div.x = op1
            self.div.y = op2
            res = self.div.execute()
        else:
            res = "Operação não suportada"
        return res

    def start_server(self, host='127.0.0.1', port=5000):
        # É feita a ligação a um porto (bind) e espera uma ligação (listen) 
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Servidor Calculadora ativo em {host}:{port}. À espera de ligações...")

        while True:
            # Aceitação da ligação 
            conn, addr = server_socket.accept()
            try:
                # Servidor recebe mensagens do tipo OBJ_OP
                msg_type = conn.recv(6).decode('utf-8')
                
                if msg_type == "OBJ_OP":
                    # Recebe o objeto dicionário e descodifica-o
                    obj = receive_object(conn)
                    
                    if obj:
                        # Retira do dicionário os valores
                        op = obj.get("oper")
                        op1 = obj.get("op1")
                        op2 = obj.get("op2")
                        
                        # Executa e devolve o valor ao cliente
                        res = self.execute_calc(op, op1, op2)
                        conn.send(str(res).encode('utf-8'))
                        
            except Exception as e:
                print(f"Erro ao processar cliente {addr}: {e}")
            finally:
                conn.close()

# Permite iniciar o servidor correndo este ficheiro diretamente
if __name__ == '__main__':
    maq = Maquina()
    maq.start_server()