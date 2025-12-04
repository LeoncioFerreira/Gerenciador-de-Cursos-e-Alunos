from flask import Flask, render_template
from routes.cursos_routes import cursos_bp
from routes.turmas_routes import turmas_bp

app = Flask(__name__)

@app.route("/") # Rota padrão
def index():
    return render_template("index.html") 

# Registrar blueprint
app.register_blueprint(cursos_bp, url_prefix="/cursos")
app.register_blueprint(turmas_bp, url_prefix="/turmas")

if __name__ == "__main__":
    app.run(debug=True)