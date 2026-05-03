from database import db
from models.produto import Produto
from models.movimentacao_produto import MovimentacaoProduto


def saida_produto(produto_id, quantidade):
    produto = Produto.query.get(produto_id)

    if not produto:
        raise Exception("Produto não encontrado")

    if quantidade <= 0:
        raise Exception("Quantidade inválida")

    if produto.estoque_atual < quantidade:
        raise Exception("Estoque insuficiente")

    # baixa no estoque
    produto.estoque_atual -= quantidade

    # registra movimentação
    mov = MovimentacaoProduto(
        produto_id=produto_id,
        tipo="saida",
        quantidade=quantidade,
        motivo="venda"
    )

    db.session.add(mov)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise