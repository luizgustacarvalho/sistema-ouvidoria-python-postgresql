
from reclamações import chamados, criar_chamado, carregar_chamados
from supervisor import Supervisor


def main():

    # Carrega as reclamações salvas no PostgreSQL
    resultado = carregar_chamados()

    if resultado is None:
        print("Não foi possível iniciar o sistema.")
        return

    supervisor = Supervisor(lista_chamados=chamados)

    while True:
        print("\n=== SISTEMA DE OUVIDORIA ===")
        print("1 - Registrar reclamação")
        print("2 - Área do supervisor")
        print("3 - Sair do sistema")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            criar_chamado()

        elif opcao == "2":
            supervisor.exibir_menu()

        elif opcao == "3":
            print("Sistema encerrado.")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
