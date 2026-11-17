from flask import Flask, abort, redirect, render_template, request, url_for

from datos import categorias, productos
from funciones import buscar_producto, calcular_resumen, filtrar_productos
from funciones import productos_para_reponer, siguiente_id, validar_producto

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("inicio.html", total=len(productos))


@app.route("/productos")
def listado():
    return render_template("listado.html", productos=productos)


@app.route("/producto/<int:identificador>")
def detalle(identificador):
    producto = buscar_producto(productos, identificador)
    if producto is None:
        abort(404)
    return render_template("detalle.html", producto=producto)


@app.route("/consulta")
def consulta():
    criterio = request.args.get("criterio", "nombre")
    valor = request.args.get("valor", "").strip()
    consultado = "criterio" in request.args or "valor" in request.args
    resultados = []
    error = ""
    if consultado:
        resultados, error = filtrar_productos(productos, criterio, valor)
    return render_template("consulta.html", criterio=criterio, valor=valor,
                           consultado=consultado, productos=resultados,
                           error=error, categorias=categorias)


@app.route("/anadir", methods=["GET", "POST"])
def anadir():
    valores = {}
    errores = []
    if request.method == "POST":
        valores = request.form
        producto, errores = validar_producto(valores)
        if not errores:
            producto["id"] = siguiente_id(productos)
            productos.append(producto)
            return redirect(url_for("detalle", identificador=producto["id"]))
    return render_template("formulario.html", valores=valores,
                           errores=errores, categorias=categorias)


@app.route("/resumen")
def resumen():
    return render_template("resumen.html", resumen=calcular_resumen(productos))


@app.route("/reposicion")
def reposicion():
    return render_template("reposicion.html", productos=productos_para_reponer(productos))


@app.errorhandler(404)
def no_encontrado(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run()
