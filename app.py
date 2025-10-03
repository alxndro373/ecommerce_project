from flask import Flask, render_template
from routes.usuarios import usuarios_bp
from routes.categorias import categorias_bp
from routes.productos import productos_bp

app = Flask(__name__)

#Blueprints
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
app.register_blueprint(categorias_bp, url_prefix="/categorias")
app.register_blueprint(productos_bp, url_prefix="/productos")

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)