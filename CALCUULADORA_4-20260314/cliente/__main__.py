from cliente.interface import Interacao
from servidor.maquinas import Maquina

def run_server():
    server = Maquina()
    server.execute()

if __name__ == "__main__":
    ui = Interacao()
    ui.execute()
