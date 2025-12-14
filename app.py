from flask import Flask, render_template
from routes.cursos_routes import cursos_bp
from routes.turmas_routes import turmas_bp
from routes.alunos_routes import alunos_bp 
from routes.matriculas_routes import matriculas_bp
from routes.relatorios_routes import relatorios_bp

app = Flask(__name__)

@app.route("/") # Rota padrão
def index():
    return render_template("index.html") 

# Registrar blueprint
app.register_blueprint(cursos_bp, url_prefix="/cursos")
app.register_blueprint(turmas_bp, url_prefix="/turmas")
app.register_blueprint(alunos_bp, url_prefix="/alunos")
app.register_blueprint(matriculas_bp, url_prefix="/matriculas")
app.register_blueprint(relatorios_bp, url_prefix="/relatorios")

if __name__ == "__main__":
    app.run(debug=True)