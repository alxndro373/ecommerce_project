from flask import Blueprint, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from config.db import db

productos_bp = Blueprint("productos", __name__)

@productos_bp.route("/")
def listar():
    productos = list(db.productos.find())
    return render_template("/views/productos.html", productos=productos)

@productos_bp.route("/crear", methods=["POST"])
def crear():
    nuevo_producto = {
        "producto_id": request.form["producto_id"],
        "nombre": request.form["nombre"],
        "descripcion": request.form["descripcion"],
        "precio": float(request.form["precio"]),
        "categoria_id": int(request.form["categoria_id"]),
        "inventario": int(request.form["inventario"]),
        "activo": request.form.get("activo") == "1"
    }
    db.productos.insert_one(nuevo_producto)
    return redirect(url_for("productos.listar"))

@productos_bp.route("/editar/<id>", methods=["POST"])
def editar(id):
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

@productos_bp.route("/eliminar/<id>")
def eliminar(id):
    db.productos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("productos.listar"))