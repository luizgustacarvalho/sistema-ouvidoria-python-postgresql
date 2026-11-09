
import psycopg
from getpass import getpass


def conectar():
    senha = getpass("Digite a senha do PostgreSQL: ")

    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="ouvidoria_db",
        user="postgres",
        password=senha
    )


def testar_conexao():
    try:
        with conectar() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("SELECT version();")
                resultado = cursor.fetchone()

                print("\nConexão estabelecida com sucesso!")
                print("PostgreSQL:", resultado[0])

    except psycopg.Error as erro:
        print("\nNão foi possível conectar ao PostgreSQL.")
        print(f"Detalhes do erro: {erro}")


def cadastrar_chamado(chamado):
    try:
        with conectar() as conexao:
            with conexao.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO chamados (
                        categoria,
                        descricao,
                        status,
                        data_abertura,
                        data_limite
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (
                        chamado.categoria,
                        chamado.descricao,
                        chamado.status,
                        chamado.data_abertura,
                        chamado.data_limite
                    )
                )

                resultado = cursor.fetchone()
                chamado.id = resultado[0]

                return chamado.id

    except psycopg.Error as erro:
        print("\nErro ao cadastrar reclamação no banco.")
        print(f"Detalhes: {erro}")
        return None


def listar_chamados():
    try:
        with conectar() as conexao:
            with conexao.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        id,
                        categoria,
                        descricao,
                        status,
                        data_abertura,
                        data_limite,
                        data_resolucao
                    FROM chamados
                    ORDER BY id;
                    """
                )

                resultados = cursor.fetchall()

                return resultados

    except psycopg.Error as erro:
        print("\nErro ao consultar reclamações no banco.")
        print(f"Detalhes: {erro}")
        return None



def atualizar_status_chamado(id_chamado, novo_status):
    try:
        with conectar() as conexao:
            with conexao.cursor() as cursor:

                cursor.execute(
                    """
                    UPDATE chamados
                    SET
                        status = %s,
                        data_resolucao = CASE
                            WHEN %s = 'Resolvido'
                            THEN CURRENT_TIMESTAMP
                            ELSE NULL
                        END
                    WHERE id = %s
                    RETURNING id, data_resolucao;
                    """,
                    (novo_status, novo_status, id_chamado)
                )

                resultado = cursor.fetchone()

                if resultado is None:
                    print("Protocolo não encontrado no banco de dados.")
                    return False, None

                data_resolucao = resultado[1]

                return True, data_resolucao

    except psycopg.Error as erro:
        print("\nErro ao atualizar o status no banco.")
        print(f"Detalhes: {erro}")
        return False, None

if __name__ == "__main__":
    resultados = listar_chamados()

    if resultados is not None:
        for chamado in resultados:
            print(chamado)
