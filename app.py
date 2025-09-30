from flask import Flask, render_template
from routes.usuarios import usuarios_bp

app = Flask(__name__)

#Blueprints
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)