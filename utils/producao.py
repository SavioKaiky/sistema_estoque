from database import db
from models.produto import Produto
from models.insumo import Insumo
from models.ficha_tecnica import FichaTecnica
from models.movimentacao_produto import MovimentacaoProduto
from models.movimentacao_insumo import MovimentacaoInsumo

def produzir(produto_id, quantidade):
    produto = Produto.query.get(produto_id)

    if not produto:
        raise Exception("Produto não encontrado")

    if quantidade <= 0:
        raise Exception("Quantidade inválida")

    ficha = FichaTecnica.query.filter_by(produto_id=produto_id).all()

    if not ficha:
        raise Exception("Produto sem ficha técnica")

    # 1. VALIDAR ESTOQUE (ANTES DE ALTERAR)
    for item in ficha:
        insumo = Insumo.query.get(item.insumo_id)
        consumo = item.quantidade * quantidade

        if insumo.estoque_atual < consumo:
            raise Exception(f"Estoque insuficiente: {insumo.nome}")

    # 2. DAR BAIXA NOS INSUMOS
    for item in ficha:
        insumo = Insumo.query.get(item.insumo_id)
        consumo = item.quantidade * quantidade

        insumo.estoque_atual -= consumo

        mov_insumo = MovimentacaoInsumo(
            insumo_id=insumo.id,
            tipo="saida",
            quantidade=consumo,
            motivo="produção"
        )
        db.session.add(mov_insumo)

    # 3. ADICIONAR PRODUTO AO ESTOQUE
    produto.estoque_atual += quantidade

    mov_produto = MovimentacaoProduto(
        produto_id=produto_id,
        tipo="entrada",
        quantidade=quantidade,
        motivo="produção"
    )
    db.session.add(mov_produto)

    db.session.commit()