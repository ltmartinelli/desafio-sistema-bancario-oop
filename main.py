import abc
from datetime import datetime
from abc import ABC, abstractmethod


class Conta:
    def __init__(self, saldo, numero, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self.saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo

        if saldo < valor:
            print(f"Saldo insuficiente! Seu saldo é de RS{saldo:.2f}")
        elif valor > 0:
            self._saldo -= valor
            print(f"Saque realizado com sucesso!")
            return True
        else:
            print("Apenas valores positivos!")

        return False

    def depositar(self, valor):
        saldo = self.saldo

        if valor < 0:
            print("Apenas valores positivos!")
        else:
            self._saldo += valor
            print("Depósito realizado com sucesso!")
            return True

        return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        n_saques = 0
        for transacao in self.historico.transacoes:
            if transacao["Tipo"] == Saque.__name__:
                n_saques += 1
        if n_saques >= self._limite_saques:
            print("Limite diário de saques atingidos!")
        if valor > self._limite:
            print("Limite para saques é de R$ 500!")
        else:
            super().sacar(valor)

        return False

    def __str__(self):
        return f"""
Agência:\t{self.agencia}
C/C:\t\t{self.numero}
Titular:\t{self.cliente.nome}
        """


class Cliente():

    def __init__(self, endereco, contas):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):

    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Historico():
    def __init__(self):
        self.transacoes = []

    @property
    def transacoes(self):
        return self.transacoes

    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "Tipo": transacao.__class__.__name__,
                "Valor": transacao.valor,
                "Data": datetime.now().strftime("%d-%m-%Y %H:%M:%s")
            }
        )


class Transacao(ABC):
    @property
    @abc.abstractmethod
    def valor(self):
        pass

    @classmethod
    @abc.abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

def main():
    menu = """
\n
================ MENU ================
[d]Depositar
[s]Sacar
[e]Extrato
[nc]Nova conta
[lc]Listar contas
[nu]Novo usuário
[q]Sair
=> """

main()

