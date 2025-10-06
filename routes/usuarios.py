from flask import Blueprint, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from config.db import db

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")

@usuarios_bp.route("/")
def listar():
    usuarios = list(db.usuarios.find())
    return render_template("/views/usuarios/index.html", usuarios=usuarios)

@usuarios_bp.route("/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        nuevo_usuario = {
            "usuario_id": int(request.form["usuario_id"]),
            "nombre": request.form["nombre"],
            "correo": request.form["correo"],
            "telefono": request.form["telefono"],
            "direccion": request.form["direccion"]
        }
        db.usuarios.insert_one(nuevo_usuario)
        return redirect(url_for("usuarios.listar"))
    return render_template("/views/usuarios/crear.html")

@usuarios_bp.route("/editar/<id>", methods=["GET", "POST"])
def editar(id):
    usuario = db.usuarios.find_one({"_id": ObjectId(id)})
    if not usuario:
        return "Usuario no encontrado", 404

    if request.method == "POST":
        db.usuarios.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "nombre": request.form["nombre"],
                "correo": request.form["correo"],
                "telefono": request.form["telefono"],
                "direccion": request.form["direccion"]
            }}
        )
        return redirect(url_for("usuarios.listar"))
    return render_template("/views/usuarios/editar.html", usuario=usuario)

@usuarios_bp.route("/eliminar/<id>")
def eliminar(id):
    db.usuarios.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("usuarios.listar"))
