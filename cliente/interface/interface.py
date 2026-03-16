import socket
import json

INT_SIZE = 4 # Tamanho fixo em bytes para o cabeçalho do tamanho da mensagem

def send_int(connection, value, size):
    """Função auxiliar para enviar o tamanho do objeto."""
    connection.send(value.to_bytes(size, byteorder='big'))

def send_object(connection, obj):
    """1º: envia tamanho, 2º: envia dados."""
    data = json.dumps(obj).encode('utf-8')
    size = len(data)
    send_int(connection, size, INT_SIZE)
    connection.send(data)

class Interface:
    def __init__(self, host='127.0.0.1', port=5000):
        # A máquina já não é recebida por parâmetro. Agora ligamo-nos remotamente.
        self.host = host
        self.port = port

    def execute(self):
        print("Qual é o cálculo que quer efetuar? x + - /")
        op = input().strip()
        print("Preciso que introduza dois valores:")
        x = float(input("x="))
        y = float(input("y="))

        # Estabelece a ligação indicando endereço e porta 
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            client_socket.connect((self.host, self.port))

            # 1. Envia string com nome da operação
            client_socket.send("OBJ_OP".encode('utf-8'))
            
            # Pequena pausa para evitar a junção de pacotes na receção
            import time
            time.sleep(0.1) 

            # 2. Envia o dicionário com os operadores
            dict_op = {"oper": op, "op1": x, "op2": y}
            send_object(client_socket, dict_op)

            # 3. Fica à espera do valor (resultado) do servidor
            res = client_socket.recv(1024).decode('utf-8')
            print(f"O valor da operação '{op}' é:", res)

        except Exception as e:
            print("Erro de comunicação com o servidor:", e)
        finally:
            client_socket.close()