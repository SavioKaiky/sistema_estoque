from flask import Blueprint, render_template, request, redirect
from database import db
from models.produto import Produto
from models.insumo import Insumo
from models.ficha_tecnica import FichaTecnica

produtos_bp = Blueprint("produtos", __name__, url_prefix="/produtos")

@produtos_bp.route("/", methods=["GET", "POST"])
def listar_produtos():
    if request.method == "POST":
        nome = request.form.get("nome")

        novo = Produto(nome=nome)
        db.session.add(novo)
        db.session.commit()

        return redirect("/produtos")

    produtos = Produto.query.all()
    return render_template("produtos/listar.html", produtos=produtos)

@produtos_bp.route("/<int:produto_id>/ficha", methods=["GET", "POST"])
def ficha(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    insumos = Insumo.query.all()

    if request.method == "POST":
        insumo_id = int(request.form.get("insumo_id"))
        quantidade = float(request.form.get("quantidade"))

        item = FichaTecnica(
            produto_id=produto_id,
            insumo_id=insumo_id,
            quantidade=quantidade
        )

        db.session.add(item)
        db.session.commit()

        return redirect(f"/produtos/{produto_id}/ficha")

    ficha = FichaTecnica.query.filter_by(produto_id=produto_id).all()

    return render_template(
        "produtos/ficha.html",
        produto=produto,
        insumos=insumos,
        ficha=ficha
    )