from flask import Blueprint, render_template, request, redirect, url_for
from config.db import db
from bson.objectid import ObjectId
from datetime import datetime

carrito_bp = Blueprint('carrito', __name__, url_prefix='/carrito')

@carrito_bp.route('/')
def index():
    carritos = list(db.carrito.find())
    usuarios = list(db.usuarios.find({}, {"usuario_id": 1, "nombre": 1}))
    productos = list(db.productos.find({}, {"producto_id": 1, "nombre": 1, "precio": 1}))
    return render_template('/views/carrito.html', carritos=carritos, usuarios=usuarios, productos=productos)


@carrito_bp.route('/crear', methods=['POST'])
def crear():
    carrito = {
        "carrito_id": int(request.form['carrito_id']),
        "usuario_id": int(request.form['usuario_id']),
        "producto_id": [int(pid) for pid in request.form.getlist('producto_id')],
        "total": float(request.form['total']),
        "fecha_actualizacion": datetime.utcnow()
    }
    db.carrito.insert_one(carrito)
    return redirect(url_for('carrito.index'))

@carrito_bp.route('/editar/<id>', methods=['POST'])
def editar(id):
    db.carrito.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "usuario_id": int(request.form['usuario_id']),
                "producto_id": [int(pid) for pid in request.form.getlist('producto_id')],
                "total": float(request.form['total']),
                "fecha_actualizacion": datetime.utcnow()
            }
        }
    )
    return redirect(url_for('carrito.index'))

@carrito_bp.route('/eliminar/<id>')
def eliminar(id):
    db.carrito.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('carrito.index'))
