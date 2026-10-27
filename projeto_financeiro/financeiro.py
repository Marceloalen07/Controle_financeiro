
import json
from pathlib import Path
from datetime import date

ARQUIVO_DADOS = Path(__file__).with_name("dados.json")


def carregar_movimentacoes():
    """Carrega as movimentações salvas no JSON."""

    if not ARQUIVO_DADOS.exists():
        return []

    try:
        with ARQUIVO_DADOS.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        if not isinstance(dados, list):
            raise ValueError("O arquivo precisa conter uma lista.")

        return dados

    except json.JSONDecodeError as erro:
        raise ValueError(
            "O arquivo dados.json está inválido. "
            "Verifique o conteúdo antes de continuar."
        ) from erro


def salvar_movimentacoes(movimentacoes):
    """Salva as movimentações no arquivo JSON."""

    with ARQUIVO_DADOS.open("w", encoding="utf-8") as arquivo:
        json.dump(
            movimentacoes,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


def adicionar_movimentacao(
    tipo, descricao, valor, categoria, data_movimentacao
):
    """Adiciona uma nova receita ou despesa."""

    if tipo not in ["Receita", "Despesa"]:
        raise ValueError("Tipo de movimentação inválido.")

    descricao = descricao.strip()
    categoria = categoria.strip()

    if not descricao:
        raise ValueError("Informe a descrição.")

    if not categoria:
        raise ValueError("Informe a categoria.")

    if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
        raise ValueError(
            "O valor deve ser positivo e estar em centavos."
        )

    try:
        data_validada = date.fromisoformat(data_movimentacao)
    except (TypeError, ValueError) as erro:
        raise ValueError(
            "Informe uma data válida no formato AAAA-MM-DD."
        ) from erro

    movimentacoes = carregar_movimentacoes()

    proximo_id = max(
        (item.get("id", 0) for item in movimentacoes),
        default=0
    ) + 1

    movimentacao = {
        "id": proximo_id,
        "tipo": tipo,
        "descricao": descricao,
        "valor_centavos": valor,
        "categoria": categoria,
        "data": data_validada.isoformat()
    }

    movimentacoes.append(movimentacao)
    salvar_movimentacoes(movimentacoes)

    return movimentacao


def excluir_movimentacao(id_movimentacao):
    """Exclui uma movimentação pelo seu ID."""

    movimentacoes = carregar_movimentacoes()

    atualizadas = [
        item for item in movimentacoes
        if item.get("id") != id_movimentacao
    ]

    if len(atualizadas) == len(movimentacoes):
        raise ValueError("Movimentação não encontrada.")

    salvar_movimentacoes(atualizadas)


def calcular_resumo(movimentacoes):
    """Calcula receitas, despesas e saldo."""

    receitas = sum(
        item["valor_centavos"]
        for item in movimentacoes
        if item["tipo"] == "Receita"
    )

    despesas = sum(
        item["valor_centavos"]
        for item in movimentacoes
        if item["tipo"] == "Despesa"
    )

    return {
        "receitas": receitas,
        "despesas": despesas,
        "saldo": receitas - despesas
    }
