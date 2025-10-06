from flask import Blueprint, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from config.db import db

productos_bp = Blueprint("productos", __name__, url_prefix="/productos")

@productos_bp.route("/")
def listar():
    productos = list(db.productos.find())
    return render_template("/views/productos/index.html", productos=productos) 

@productos_bp.route("/crear", methods=["GET", "POST"])
def crear():
    categorias = list(db.categorias.find())
    if request.method == "POST":
        nuevo_producto = {
            "producto_id": int(request.form["producto_id"]),
            "nombre": request.form["nombre"],
            "descripcion": request.form["descripcion"],
            "precio": float(request.form["precio"]),
            "categoria_id": [int(pid) for pid in request.form.getlist("categoria_id")],
            "inventario": int(request.form["inventario"]),
            "activo": request.form.get("activo") == "1"
        }
        db.productos.insert_one(nuevo_producto)
        return redirect(url_for("productos.listar"))
    return render_template("/views/productos/crear.html", categorias=categorias)

@productos_bp.route("/editar/<id>", methods=["GET", "POST"])
def editar(id):
    producto = db.productos.find_one({"_id": ObjectId(id)})
    categoria = list(db.categorias.find())
    if not producto:
        return "Producto no encontrado", 404
    
    if request.method == "POST":
        db.productos.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "nombre": request.form["nombre"],
                "descripcion": request.form["descripcion"],
            "precio": float(request.form["precio"]),
            "categoria_id": int(request.form["categoria_id"]),
            "inventario": int(request.form["inventario"]),
            "activo": request.form.get("activo") == "1"
            }}
        )
        return redirect(url_for("productos.listar"))
    return render_template("/views/productos/editar.html", producto=producto, categoria=categoria)

@productos_bp.route("/eliminar/<id>")
def eliminar(id):
    db.productos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("productos.listar"))