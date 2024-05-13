import abc
from datetime import datetime
from abc import ABC, abstractmethod


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

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
        saldo = self._saldo

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
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["Tipo"] == Saque.__name__]
        )

        if numero_saques >= self._limite_saques:
            print("Limite diário de saques atingidos!")
            return False
        elif valor > self._limite:
            print("Limite para saques é de R$ 500!")
            return False
        else:
            super().sacar(valor)
            return True


    def __str__(self):
        return f"""
Agência:\t{self.agencia}
C/C:\t\t{self.numero}
Titular:\t{self.cliente.nome}
        """


class Cliente():

    def __init__(self, endereco):
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
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "Tipo": transacao.__class__.__name__,
                "Valor": transacao.valor,
                "Data": datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")
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
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


def menu():
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
    return menu


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = procurar_cliente(cpf, clientes)
    if not cliente:
        print("\nCliente não encontrado!")
        return

    numero = int(input("Digite o número da conta: "))
    conta = recuperar_conta_cliente(cliente, numero)
    if not conta:
        print("\nConta não encontrado!")
        return

    valor = float(input('Digite o valor a ser depositado: '))
    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = procurar_cliente(cpf, clientes)
    if not cliente:
        print("\nCliente não encontrado!")
        return

    numero = int(input("Digite o número da conta: "))
    conta = recuperar_conta_cliente(cliente, numero)
    if not conta:
        print("\nConta não encontrado!")
        return

    valor = float(input('Digite o valor a ser sacado: '))
    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)


def procurar_cliente(cpf, clientes):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
        else:
            return None


def recuperar_conta_cliente(cliente, numero):
    if not cliente.contas:
        print('\nSem contas associadas a este cliente!')
        return
    else:
        conta = [cc for cc in cliente.contas if cc.numero == numero]
        if not conta:
            print("Conta inexistente, verifique o número da conta.")
        else:
            return conta[0]


def listar_contas(contas):
    if not contas:
        print("Não existem contas no sistema.")
    else:
        for conta in contas:
            print('#' * 100)
            print(conta)


def criar_usuario(clientes):
    print("Insira os dados de cadastro:")
    cpf = input("CPF: ")
    cliente = procurar_cliente(cpf, clientes)
    if cliente:
        print("CPF já cadastrado!")
        return

    nome = input("Nome: ")
    endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    data_nascimento = input("Data de Nascimento (dd/mm/aaaa): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("\n Cliente cadastrado com sucesso!")


def criar_conta(clientes, contas):
    cpf = input("CPF do cliente: ")
    cliente = procurar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    numero = len(contas) + 1
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero)
    contas.append(conta)
    cliente.contas.append(conta)
    print("\nConta criada com sucesso!")


def imprimir_extrato(clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = procurar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    numero = int(input("Digite o número da conta: "))

    conta = recuperar_conta_cliente(cliente, numero)
    if not conta:
        print("\nConta não encontrado!")
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['Tipo']}:\n\tR$ {transacao['Valor']:.2f}"

    print(extrato)
    print("==========================================")
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def main():
    clientes = []
    contas = []

    while True:

        opcao = input(menu())

        if opcao == 'd':
            depositar(clientes)
        elif opcao == 's':
            sacar(clientes)
        elif opcao == 'e':
            imprimir_extrato(clientes, contas)
        elif opcao == 'nc':
            criar_conta(clientes, contas)
        elif opcao == 'lc':
            listar_contas(contas)
        elif opcao == 'nu':
            criar_usuario(clientes)
        elif opcao == 'q':
            break
        else:
            print('\nOpção inválida!')


main()
