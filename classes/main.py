from Client import Cliente
from Garcom import Garcom
from Gerenciamento import Gerenciamento

def recolhendo_data():
    clientN = input("Quantdade de clientes: ")
    garcomN = input("Quantidade de garcons: ")
    rodadas = input("Número de rodadas permitidas: ")

    return int(clientN), int(garcomN), int(rodadas)

try:
    clientN, garcomN, rodadas = recolhendo_data()

    management = [Gerenciamento(n, rodadas) for n in range(rodadas)]
    garcom = [Garcom(3, n, management) for n in range(0, garcomN)]
    cliente = [Cliente(n, management) for n in range(clientN)]
    
    for x in garcom:
        x.start()
    for x in cliente:
        x.start()

    for x in cliente:
        x.join()
    
    for x in garcom:
        x.join()
except Exception as e:
    print(e)
