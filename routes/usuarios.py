from flask import Blueprint, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from config.db import db

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("/")
def listar():
    usuarios = list(db.usuarios.find())
    return render_template("/views/usuarios.html", usuarios=usuarios)

@usuarios_bp.route("/crear", methods=["POST"])
def crear():
    nuevo_usuario = {
        "usuario_id": request.form["usuario_id"],
        "nombre": request.form["nombre"],
        "correo": request.form["correo"],
        "telefono": request.form["telefono"],
        "direccion": request.form["direccion"]
    }
    db.usuarios.insert_one(nuevo_usuario)
    return redirect(url_for("usuarios.listar"))

@usuarios_bp.route("/editar/<id>", methods=["POST"])
def editar(id):
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

@usuarios_bp.route("/eliminar/<id>")
def eliminar(id):
    db.usuarios.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("usuarios.listar"))