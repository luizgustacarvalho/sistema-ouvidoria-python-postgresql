
import os
from datetime import datetime

from dotenv import load_dotenv
from banco_dados import atualizar_status_chamado


load_dotenv()


class Supervisor:
    STATUS_DISPONIVEIS = {
        "1": "Pendente",
        "2": "Em andamento",
        "3": "Resolvido"
    }

    def __init__(self, lista_chamados):
        self.lista_chamados = lista_chamados
        self.senha = os.getenv("SUPERVISOR_PASSWORD")

        if not self.senha:
            raise RuntimeError(
                "Senha do supervisor não configurada. "
                "Verifique o arquivo .env."
            )

    def autenticar(self):
        tentativas = 3

        while tentativas > 0:
            senha_digitada = input("Digite a senha do supervisor: ")

            if senha_digitada == self.senha:
                print("\nAcesso autorizado!")
                return True

            tentativas -= 1
            print(f"Senha incorreta. Tentativas restantes: {tentativas}")

        print("\nAcesso bloqueado.")
        return False

    def buscar_chamado(self, protocolo):
        for chamado in self.lista_chamados:
            if chamado.id == protocolo:
                return chamado

        return None

    def solicitar_protocolo(self):
        try:
            protocolo = int(input("Digite o número do protocolo: ").strip())

            if protocolo <= 0:
                print("O protocolo deve ser um número positivo.")
                return None

            return protocolo

        except ValueError:
            print("Protocolo inválido. Digite um número inteiro.")
            return None

    def obter_situacao_prazo(self, chamado):
        if chamado.status == "Resolvido":
            return "Resolvida"

        if chamado.esta_atrasado():
            return "ATRASADO"

        if datetime.now().date() == chamado.data_limite:
            return "Vence hoje"

        return "Dentro do prazo"

    def verificar_alertas_prazo(self):
        chamados_atrasados = [
            chamado
            for chamado in self.lista_chamados
            if chamado.esta_atrasado()
        ]

        print("\n" + "=" * 45)
        print("          ALERTA DE PRAZOS")
        print("=" * 45)

        if not chamados_atrasados:
            print("Nenhuma reclamação está atrasada.")
            print("=" * 45)
            return

        print(
            f"ATENÇÃO: {len(chamados_atrasados)} "
            "reclamação(ões) ultrapassaram o prazo!"
        )

        for chamado in chamados_atrasados:
            print("\n" + "-" * 40)
            print(f"Protocolo: {chamado.id}")
            print(f"Categoria: {chamado.categoria}")
            print(f"Status: {chamado.status}")
            print(
                "Prazo final: "
                f"{chamado.data_limite.strftime('%d/%m/%Y')}"
            )
            print(
                "Dias úteis em atraso: "
                f"{chamado.calcular_dias_atraso()}"
            )

        print("=" * 45)

    def exibir_detalhes_chamado(self, chamado):
        print("\n" + "=" * 45)
        print(f"PROTOCOLO: {chamado.id}")
        print("=" * 45)

        print(f"Categoria: {chamado.categoria}")
        print(f"Descrição: {chamado.descricao}")
        print(f"Status: {chamado.status}")

        print(
            "Data de abertura: "
            f"{chamado.data_abertura.strftime('%d/%m/%Y %H:%M')}"
        )

        print(
            "Prazo interno: "
            f"{chamado.data_limite.strftime('%d/%m/%Y')}"
        )

        print(f"Situação do prazo: {self.obter_situacao_prazo(chamado)}")

        if chamado.status == "Resolvido":
            if chamado.data_resolucao is not None:
                print(
                    "Data de resolução: "
                    f"{chamado.data_resolucao.strftime('%d/%m/%Y %H:%M')}"
                )
        else:
            print(
                "Dias úteis pendentes: "
                f"{chamado.calcular_dias_pendentes()}"
            )

            print(
                "Dias úteis restantes: "
                f"{chamado.calcular_dias_restantes()}"
            )

            if chamado.esta_atrasado():
                print(
                    "DIAS ÚTEIS EM ATRASO: "
                    f"{chamado.calcular_dias_atraso()}"
                )

        print("=" * 45)

    def exibir_chamados(self, filtro=None):
        print("\n=== CONSULTA DE RECLAMAÇÕES ===")

        chamados_encontrados = [
            chamado
            for chamado in self.lista_chamados
            if filtro is None or chamado.status == filtro
        ]

        if not chamados_encontrados:
            print("Nenhuma reclamação encontrada.")
            return

        for chamado in chamados_encontrados:
            self.exibir_detalhes_chamado(chamado)

    def exibir_reclamacoes_em_aberto(self):
        print("\n=== RECLAMAÇÕES EM ABERTO ===")

        chamados_abertos = [
            chamado
            for chamado in self.lista_chamados
            if chamado.status in ("Pendente", "Em andamento")
        ]

        if not chamados_abertos:
            print("Não existem reclamações em aberto.")
            return

        for chamado in chamados_abertos:
            self.exibir_detalhes_chamado(chamado)

    def alterar_status(self):
        print("\n=== ALTERAÇÃO DE STATUS ===")

        if not self.lista_chamados:
            print("Não existem reclamações cadastradas.")
            return

        protocolo = self.solicitar_protocolo()

        if protocolo is None:
            return

        chamado = self.buscar_chamado(protocolo)

        if chamado is None:
            print("Protocolo não encontrado.")
            return

        self.exibir_detalhes_chamado(chamado)

        if chamado.status == "Resolvido":
            print(
                "\nEsta reclamação já foi resolvida. "
                "A reabertura ainda não está disponível."
            )
            return

        print("\nStatus disponíveis:")

        for opcao, status in self.STATUS_DISPONIVEIS.items():
            print(f"{opcao} - {status}")

        opcao = input("Escolha o novo status: ").strip()

        if opcao not in self.STATUS_DISPONIVEIS:
            print("Opção inválida. O status não foi alterado.")
            return

        novo_status = self.STATUS_DISPONIVEIS[opcao]

        if novo_status == chamado.status:
            print("A reclamação já possui esse status.")
            return

        sucesso, data_resolucao = atualizar_status_chamado(
            chamado.id,
            novo_status
        )

        if not sucesso:
            print(
                "Não foi possível atualizar a reclamação. "
                "O status original foi mantido."
            )
            return

        chamado.status = novo_status
        chamado.data_resolucao = data_resolucao

        print("\nStatus atualizado e salvo no PostgreSQL!")
        print(f"Novo status: {chamado.status}")

    def ver_estatisticas(self):
        total = len(self.lista_chamados)

        pendentes = 0
        em_andamento = 0
        resolvidos = 0
        atrasados = 0

        for chamado in self.lista_chamados:
            if chamado.status == "Pendente":
                pendentes += 1

            elif chamado.status == "Em andamento":
                em_andamento += 1

            elif chamado.status == "Resolvido":
                resolvidos += 1

            if chamado.esta_atrasado():
                atrasados += 1

        em_aberto = pendentes + em_andamento

        print("\n" + "=" * 40)
        print("       ESTATÍSTICAS DA OUVIDORIA")
        print("=" * 40)

        print(f"Total de reclamações: {total}")
        print(f"Reclamações em aberto: {em_aberto}")
        print(f"Pendentes: {pendentes}")
        print(f"Em andamento: {em_andamento}")
        print(f"Resolvidas: {resolvidos}")
        print(f"Fora do prazo: {atrasados}")

        if total > 0:
            percentual_resolvido = (resolvidos / total) * 100
            print(
                "Percentual resolvido: "
                f"{percentual_resolvido:.1f}%"
            )

        print("=" * 40)

    def exibir_menu(self):
        if not self.autenticar():
            return

        self.verificar_alertas_prazo()

        while True:
            print("\n" + "=" * 40)
            print("          ÁREA DO SUPERVISOR")
            print("=" * 40)
            print("1 - Ver todas as reclamações")
            print("2 - Ver reclamações em aberto")
            print("3 - Ver reclamações pendentes")
            print("4 - Ver reclamações em andamento")
            print("5 - Alterar status de uma reclamação")
            print("6 - Ver estatísticas")
            print("7 - Sair da área do supervisor")

            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self.exibir_chamados()

            elif opcao == "2":
                self.exibir_reclamacoes_em_aberto()

            elif opcao == "3":
                self.exibir_chamados(filtro="Pendente")

            elif opcao == "4":
                self.exibir_chamados(filtro="Em andamento")

            elif opcao == "5":
                self.alterar_status()

            elif opcao == "6":
                self.ver_estatisticas()

            elif opcao == "7":
                print("Saindo da área do supervisor...")
                break

            else:
                print("Opção inválida. Escolha uma opção de 1 a 7.")
