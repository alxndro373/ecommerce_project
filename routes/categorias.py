from flask import Blueprint, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from config.db import db

categorias_bp = Blueprint("categorias", __name__)

@categorias_bp.route("/")
def listar():
    categorias = list(db.categorias.find())
    return render_template("views/categorias.html", categorias=categorias)

@categorias_bp.route("/crear", methods=["POST"])
def crear():
    nueva_categoria = {
        "categoria_id": request.form["categoria_id"],
        "nombre": request.form["nombre"],
        "descripcion": request.form["descripcion"],
        "activa": request.form.get("activa") == "1"
    }
    db.categorias.insert_one(nueva_categoria)
    return redirect(url_for("categorias.listar"))

@categorias_bp.route("/editar/<id>", methods=["POST"])
def editar(id):
    db.categorias.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "nombre": request.form["nombre"],
            "descripcion": request.form["descripcion"],
            "activa": request.form.get("activa") == "1"
        }}
    )
    return redirect(url_for("categorias.listar"))

@categorias_bp.route("/eliminar/<id>")
def eliminar(id):
    db.categorias.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("categorias.listar"))