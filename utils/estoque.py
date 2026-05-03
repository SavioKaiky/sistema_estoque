from database import db
from models.insumo import Insumo
from models.movimentacao_insumo import MovimentacaoInsumo


def movimentar_insumo(insumo_id, tipo, quantidade, motivo):
    insumo = Insumo.query.get(insumo_id)

    if not insumo:
        raise Exception("Insumo não encontrado")

    if quantidade <= 0:
        raise Exception("Quantidade inválida")

    # SAÍDA (validação de estoque)
    if tipo == "saida":
        if insumo.estoque_atual < quantidade:
            raise Exception("Estoque insuficiente")

        insumo.estoque_atual -= quantidade

    elif tipo == "entrada":
        insumo.estoque_atual += quantidade

    else:
        raise Exception("Tipo inválido")

    mov = MovimentacaoInsumo(
        insumo_id=insumo_id,
        tipo=tipo,
        quantidade=quantidade,
        motivo=motivo
    )

    db.session.add(mov)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise