from flask import Blueprint, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from config.db import db

categorias_bp = Blueprint("categorias", __name__, url_prefix="/categorias")

@categorias_bp.route("/")
def listar():
    categorias = list(db.categorias.find())
    return render_template("/views/categorias/index.html", categorias=categorias)

@categorias_bp.route("/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        nueva_categoria = {
            "categoria_id": int(request.form["categoria_id"]),
            "nombre": request.form["nombre"],
            "descripcion": request.form["descripcion"],
            "activa": request.form.get("activa") == "1"
        }
        db.categorias.insert_one(nueva_categoria)
        return redirect(url_for("categorias.listar"))
    return render_template("/views/categorias/crear.html")

@categorias_bp.route("/editar/<id>", methods=["GET", "POST"])
def editar(id):
    categoria = db.categorias.find_one({"_id": ObjectId(id)})
    if not categoria:
        return "Categoría no encontrada", 404
    
    if request.method == "POST":
        db.categorias.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "nombre": request.form["nombre"],
                "descripcion": request.form["descripcion"],
                "activa": request.form.get("activa") == "1"
        }}
        )
        return redirect(url_for("categorias.listar"))
    return render_template("/views/categorias/editar.html", categoria=categoria)

@categorias_bp.route("/eliminar/<id>")
def eliminar(id):
    db.categorias.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("categorias.listar"))