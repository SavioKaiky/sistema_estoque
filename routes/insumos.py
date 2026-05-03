from flask import Blueprint, render_template, request, redirect
from database import db
from models.insumo import Insumo
from utils.estoque import movimentar_insumo
from models.movimentacao_insumo import MovimentacaoInsumo


insumos_bp = Blueprint("insumos", __name__, url_prefix="/insumos")


@insumos_bp.route("/", methods=["GET", "POST"])
def listar_insumos():
    if request.method == "POST":
        nome = request.form.get("nome")
        unidade = request.form.get("unidade")
        estoque_minimo = request.form.get("estoque_minimo")

        novo = Insumo(
            nome=nome,
            unidade=unidade,
            estoque_minimo=float(estoque_minimo or 0)
        )

        db.session.add(novo)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise

        return redirect("/insumos")

    insumos = Insumo.query.all()
    return render_template("insumos/listar.html", insumos=insumos)

@insumos_bp.route("/movimentar", methods=["POST"])
def movimentar():
    insumo_id = int(request.form.get("insumo_id"))
    tipo = request.form.get("tipo")
    quantidade = float(request.form.get("quantidade"))
    motivo = request.form.get("motivo")

    try:
        movimentar_insumo(insumo_id, tipo, quantidade, motivo)
    except Exception as e:
        return str(e)

    return redirect("/insumos")

@insumos_bp.route("/historico")
def historico():
    movs = MovimentacaoInsumo.query.order_by(
        MovimentacaoInsumo.created_at.desc()
    ).all()

    return render_template("insumos/historico.html", movs=movs)