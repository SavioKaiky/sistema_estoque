from flask import Blueprint, render_template, request, redirect
from database import db
from models.produto import Produto
from models.insumo import Insumo
from models.ficha_tecnica import FichaTecnica
from models.movimentacao_produto import MovimentacaoProduto
from models.movimentacao_insumo import MovimentacaoInsumo
from utils.produto_saida import saida_produto
from utils.produto_saida import saida_produto
from utils.producao import produzir

produtos_bp = Blueprint("producao", __name__, url_prefix="/producao")
producao_bp = Blueprint("producao", __name__, url_prefix="/producao")

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

@producao_bp.route("/venda", methods=["GET", "POST"])
def venda():
    produtos = Produto.query.all()

    if request.method == "POST":
        produto_id = int(request.form.get("produto_id"))
        quantidade = int(request.form.get("quantidade"))

        try:
            saida_produto(produto_id, quantidade)
        except Exception as e:
            return str(e)

        return redirect("/producao/venda")

    return render_template("producao/venda.html", produtos=produtos)

@producao_bp.route("/", methods=["GET", "POST"])
def produzir_view():
    produtos = Produto.query.all()

    if request.method == "POST":
        produto_id = int(request.form.get("produto_id"))
        quantidade = int(request.form.get("quantidade"))

        try:
            produzir(produto_id, quantidade)
        except Exception as e:
            return str(e)

        return redirect("/producao")

    return render_template("producao/produzir.html", produtos=produtos)
