
from reclamações import Chamado


def test_criar_chamado():
    chamado = Chamado(
        id_chamado=1,
        categoria="Cartão",
        descricao="Compra não reconhecida"
    )

    assert chamado.id == 1
    assert chamado.categoria == "Cartão"
    assert chamado.descricao == "Compra não reconhecida"
    assert chamado.status == "Pendente"
    assert chamado.data_resolucao is None


def test_resolver_chamado():
    chamado = Chamado(
        id_chamado=1,
        categoria="Cartão",
        descricao="Compra não reconhecida"
    )

    chamado.resolver()

    assert chamado.status == "Resolvido"
    assert chamado.data_resolucao is not None

def test_nao_resolver_chamado_duas_vezes():
        chamado = Chamado(
            id_chamado=1,
            categoria="Cartão",
            descricao="Compra não reconhecida"
        )

        chamado.resolver()
        data_resolucao_original = chamado.data_resolucao

        chamado.resolver()

        assert chamado.status == "Resolvido"
        assert chamado.data_resolucao == data_resolucao_original

import pytest


def test_nao_criar_chamado_com_descricao_vazia():
    with pytest.raises(ValueError):
        Chamado(
            id_chamado=1,
            categoria="Cartão",
            descricao=""
        )


def test_nao_criar_chamado_com_apenas_espacos():
    with pytest.raises(ValueError):
        Chamado(
            id_chamado=1,
            categoria="Cartão",
            descricao="   "
        )

def test_nao_criar_chamado_com_categoria_invalida():
    with pytest.raises(ValueError):
        Chamado(
                    id_chamado=1,
                    categoria="Empréstimo inexistente",
                    descricao="Problema no serviço"
                )