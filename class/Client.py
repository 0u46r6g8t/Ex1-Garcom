import threading
import random
import logging
import time

class Cliente(threading.Thread):

    def __init__(self, nomeCliente, gerenciamento):
        threading.Thread.__init__(self)
        self.nome = nomeCliente
        self.gerecia = gerenciamento
        self.time_sleep = threading.Event()
        self.vai_beber = True

    def realizarPedido(self):
        aux = random.randint(0, 3)

        if (aux == 3):
            self.vai_beber = False
            self.gerecia.setBebida(self)
            self.time_sleep.wait()
            self.time_sleep.clear()

            logging.info(
                " ".join(['Cliente', str(self.nome), "Não vai beber"]))
            self.gerecia.esperaBebida()
        else:
            self.vai_beber = True
            self.gerecia.realizarPedido(self)

    def esperaPedido(self):
        self.time_sleep.wait()
        self.time_sleep.clear()
    
    def recebePedido(self):
        timeAux = random.randint(1, 3)
        time.sleep(timeAux)
        logging.info(' '.join(["Cliente", str(self.nome), "está bebendo"]))

    def consumirPedido(self):

        tempoAux = random.randint(1,3)
        time.sleep(tempoAux)
        logging.info(' '.join(["Cliente", str(self.nome)]))
        self.gerecia.esperaBebida()

    def execute(self):
        while not self.gerecia.close():
            self.realizarPedido()
            if(self.vai_beber):
                self.esperaPedido()
                self.recebePedido()
                self.consumirPedido()

