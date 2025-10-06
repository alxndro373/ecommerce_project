from flask import Blueprint, render_template, request, redirect, url_for
from config.db import db
from bson.objectid import ObjectId
from datetime import datetime

carrito_bp = Blueprint('carrito', __name__, url_prefix='/carrito')

@carrito_bp.route('/')
def listar():
    carritos = list(db.carrito.find())
    return render_template('/views/carrito/index.html', carritos=carritos)


@carrito_bp.route('/crear', methods=['GET','POST'])
def crear():
    usuarios = list(db.usuarios.find({}, {"usuario_id": 1, "nombre": 1}))
    productos = list(db.productos.find({}, {"producto_id": 1, "nombre": 1, "precio": 1}))
    if request.method == 'POST':
        nuevo_carrito = {
            "carrito_id": int(request.form['carrito_id']),
            "usuario_id": [int(uid) for uid in request.form.getList('usuario_id')],
            "producto_id": [int(pid) for pid in request.form.getlist('producto_id')],
            "total": float(request.form['total']),
            "fecha_actualizacion": datetime.utcnow()
        }
        db.carrito.insert_one(nuevo_carrito)
        return redirect(url_for('carrito.listar'))
    return render_template("/views/carrito/crear.html", usuarios=usuarios, productos=productos)

@carrito_bp.route('/editar/<id>', methods=['GET','POST'])
def editar(id):
    carrito = db.carrito.find_one({"_id": ObjectId(id)})
    usuario = list(db.usuarios.find({}, {"usuario_id": 1, "nombre": 1}))
    producto = list(db.productos.find({}, {"producto_id": 1, "nombre": 1, "precio": 1}))
    
    if not carrito:
        return "Carrito no encontrado", 404
    
    if request.method == "POST":
        db.carrito.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "usuario_id": [int(uid) for uid in request.form.getlist('usuario_id')],
                    "producto_id": [int(pid) for pid in request.form.getlist('producto_id')],
                    "total": float(request.form['total']),
                    "fecha_actualizacion": datetime.utcnow()
                }
            }
        )
        return redirect(url_for('carrito.listar'))
    return render_template("/views/carrito/editar.html", carrito=carrito, usuario=usuario, producto=producto)

@carrito_bp.route('/eliminar/<id>')
def eliminar(id):
    db.carrito.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('carrito.listar'))
