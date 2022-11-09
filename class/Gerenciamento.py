import threading
import logging

class Gerenciamento():
    def __init__(self, qntClientes, x):
        self.pedidos_buffe_anotados = []
        self.pedidos_nao_quer_agua = []
        self.total_entregas = 0
        self.total_anotado = 0
        self.total_rodata = x
        self.rodada = 0
        self.qntClientesSemBeber = qntClientes
        self.faltaBber = qntClientes
        self.lock = threading.Condition()
        self.vazio = threading.Semaphore(1)
        self.cheio = threading.Semaphore(0)
        self.lock_espera_beberem = threading.Condition()
        self.lock_anotacoes = threading.Condition()

    def esperaBber(self):

        with self.lock_espera_beberem:

            if (self.faltaBber - 1 == 0):
                self.faltaBber = self.qntClientesSemBeber
                self.rodada += 1

                if (self.rodada == self.total_rodata):
                    logging.info("Acabaram os pedidos")
                else:
                    self.total_anotado =  0
                    logging.info(" ".join(["Rodada ativa: ", str(self.rodada + 1)]))

                self.lock_espera_beberem.notifyAll()
            else:
                self.faltaBber -= 1
                self.lock_espera_beberem.wait()

    def close(self):
        return self.total_rodata == self.rodada

    def realizarPedido(self, client):
        self.vazio.acquire()
        with self.lock:
            self.pedidos_buffe_anotados.append(client)
        self.cheio.release()

    def not_bebida(self, cliente):
        self.vazio.acquire()
        with self.lock:
            self.pedidos_buffe_anotados.append(cliente)

        self.cheio.release()


    def anotar_pedido(self, garcom):
        with self.lock_anotacoes:
            if(self.total_anotado < self.qntClientesSemBeber):
                self.cheio.acquire()
                with self.lock:

                    if len(self.pedidos_buffe_anotados) == 1:
                        atendido = self.pedidos_buffe_anotados.pop()
                    else:
                        atendido = self.pedidos_buffe_anotados.pop()

                    self.vazio.release()
                    self.total_anotado += 1

                    return atendido
            else:
                return None
        