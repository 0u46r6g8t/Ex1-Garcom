import threading
import random
import logging
import time


class Garcom(threading.Thread):
    def __init__(self, nome, clientes, gerenciamento):
        threading.Thread.__init__(self)
        self.nome = nome
        self.gerenciamento = gerenciamento
        self.clientes = clientes
        self.pedidos_anotados = []

    def recebe_todos_os_pedidos(self):
        qnt = len(self.pedidos_anotados)

        while qnt < self.clientes:
            client = self.gerenciamento.recolher_pedido(self)

            if client is not None:
                if client.beber:
                    self.pedidos_anotados.append(client)
                    # logging.info(' '.join(["Garcom", str(self.nome), "Recebeu um pedido do cliente: {}".format(client)]))
                else:
                    client.execute()
            else:
                break

    def recebePedido(self):
        if (len(self.pedidos_anotados) > 0):
            timeAux = random.randint(1, 3)
            time.sleep(timeAux)

    def consumirPedido(self):
        for i in self.pedidos_anotados:
            i.execute()
            logging.info(
                ''.join(['Garcom', str(self.nome), 'Entregou para o cliente: ', str(i.nome)]))

    def execute(self):
        while not self.gerenciamento.close():
            self.recebe_todos_os_pedidos()
            self.recebePedido()
            self.consumirPedido()