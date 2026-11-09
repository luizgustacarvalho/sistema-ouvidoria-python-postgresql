
from datetime import datetime
from banco_dados import cadastrar_chamado, listar_chamados
from feriados import (
    adicionar_dias_uteis,
    contar_dias_uteis
)


class Chamado:
    PRAZO_DIAS_UTEIS = 5

    CATEGORIAS_VALIDAS = {
        "Aplicativo",
        "Cartão",
        "Outro serviço",
        "Outro assunto"
    }

    def __init__(self, id_chamado, categoria, descricao):

        if categoria not in self.CATEGORIAS_VALIDAS:
            raise ValueError("Categoria inválida.")

        if not descricao or not descricao.strip():
            raise ValueError("A descrição não pode ficar vazia.")

        self.id = id_chamado
        self.categoria = categoria
        self.descricao = descricao.strip()
        self.status = "Pendente"

        self.data_abertura = datetime.now()
        self.data_resolucao = None
        self.data_limite = self.calcular_data_limite()

    def calcular_data_limite(self):
        data_abertura = self.data_abertura.date()

        return adicionar_dias_uteis(
            data_abertura,
            self.PRAZO_DIAS_UTEIS
        )

    def calcular_dias_pendentes(self):
        if self.status == "Resolvido":
            return 0

        hoje = datetime.now().date()

        return contar_dias_uteis(
            self.data_abertura.date(),
            hoje
        )

    def calcular_dias_restantes(self):
        if self.status == "Resolvido":
            return 0

        hoje = datetime.now().date()

        if hoje >= self.data_limite:
            return 0

        return contar_dias_uteis(
            hoje,
            self.data_limite
        )

    def esta_atrasado(self):
        if self.status == "Resolvido":
            return False

        return datetime.now().date() > self.data_limite

    def calcular_dias_atraso(self):
        if not self.esta_atrasado():
            return 0

        hoje = datetime.now().date()

        return contar_dias_uteis(
            self.data_limite,
            hoje
        )

    def resolver(self):
        if self.status == "Resolvido":
            print("Esta reclamação já está resolvida.")
            return

        self.status = "Resolvido"
        self.data_resolucao = datetime.now()

        print("Reclamação resolvida com sucesso!")


# Lista utilizada pelo sistema enquanto o programa está aberto
chamados = []


def carregar_chamados():
    resultados = listar_chamados()

    if resultados is None:
        print("Não foi possível carregar as reclamações.")
        return None

    chamados.clear()

    for registro in resultados:
        (
            id_chamado,
            categoria,
            descricao,
            status,
            data_abertura,
            data_limite,
            data_resolucao
        ) = registro

        chamado = Chamado(
            id_chamado=id_chamado,
            categoria=categoria,
            descricao=descricao
        )

        # Restaura os dados originais do PostgreSQL
        chamado.status = status
        chamado.data_abertura = data_abertura
        chamado.data_limite = data_limite
        chamado.data_resolucao = data_resolucao

        chamados.append(chamado)

    print(f"{len(chamados)} reclamação(ões) carregada(s).")

    return chamados


def criar_chamado():

    print("\n=== ABERTURA DE RECLAMAÇÃO ===")
    print("1 - Problema no aplicativo")
    print("2 - Problema com cartão")
    print("3 - Problema em outro serviço")
    print("4 - Outro assunto")

    categorias = {
        "1": "Aplicativo",
        "2": "Cartão",
        "3": "Outro serviço",
        "4": "Outro assunto"
    }

    categoria_escolhida = input("Escolha a categoria: ").strip()

    if categoria_escolhida not in categorias:
        print("Opção inválida. Reclamação não registrada.")
        return

    descricao = input("Descreva o problema: ").strip()

    if not descricao:
        print("A descrição não pode ficar vazia.")
        return

    chamado = Chamado(
        id_chamado=None,
        categoria=categorias[categoria_escolhida],
        descricao=descricao
    )

    protocolo = cadastrar_chamado(chamado)

    if protocolo is None:
        print("Não foi possível registrar a reclamação.")
        return

    chamados.append(chamado)

    print("\nReclamação registrada com sucesso!")
    print(f"Protocolo: {chamado.id}")

    print(
        "Data de abertura: "
        f"{chamado.data_abertura.strftime('%d/%m/%Y %H:%M')}"
    )

    print(
        "Prazo interno para resolução: "
        f"{chamado.data_limite.strftime('%d/%m/%Y')}"
    )

    print(f"Meta: {Chamado.PRAZO_DIAS_UTEIS} dias úteis")
