from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'amoprogramar:)'

usuarios = {
    'ray@g.com': 'senha123'
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
dmwqkldlkqwmdçk    

class Funcionarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    cargo = db.Column(db.String(100), nullable=False)
    salario = db.Column(db.Float, nullable=False)
    ocupacao = db.Column(db.String(100), nullable=False)
    modelo_de_trabalho = db.Column(db.String(50), nullable=False)

    def __init__(self, cpf, cargo, salario, ocupacao, modelo_de_trabalho):
        self.cpf = cpf
        self.cargo = cargo
        self.salario = salario
        self.ocupacao = ocupacao
        self.modelo_de_trabalho = modelo_de_trabalho

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_solucao = db.Column(db.String(100), nullable=False)
    descricao_solucao = db.Column(db.String(200), nullable=False)
    consultor_disponivel = db.Column(db.Boolean, default=True)
    preco = db.Column(db.Float, nullable=False)

    def __init__(self, nome_solucao, descricao_solucao, consultor_disponivel, preco):
        self.nome_solucao = nome_solucao
        self.descricao_solucao = descricao_solucao
        self.consultor_disponivel = consultor_disponivel
        self.preco = preco

@app.route('/cadastro')
def cadastro():
    funcionarios = Funcionarios.query.all()
    return render_template('index.html', funcionarios=funcionarios)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['password']

    if email in usuarios and usuarios[email] == senha:
        session['usuario'] = email
        return redirect(url_for('home'))
    else:
        flash('E-mail ou senha inválidos. Tente novamente.')
        return redirect(url_for('index'))

@app.route('/home')
def home():
    if 'usuario' not in session:
        return redirect(url_for('index'))
    return render_template('home.html')
@app.route('/add_funcionario', methods=['GET'])
def show_add_funcionario_form():
    return render_template('cadatro.html')  # Um formulário HTML

# Rota POST para adicionar o funcionário
@app.route('/add_funcionario', methods=['POST'])
def add_funcionario():
    cpf = request.form['cpf']
    cargo = request.form['cargo']
    salario = float(request.form['salario'])
    ocupacao = request.form['ocupacao']
    modelo_de_trabalho = request.form['modelo_de_trabalho']

    novo_funcionario = Funcionarios(cpf, cargo, salario, ocupacao, modelo_de_trabalho)
    db.session.add(novo_funcionario)
    db.session.commit()

    return redirect(url_for('cadastro'))

@app.route('/servicos')
def servicos():
    servicos = Servico.query.all()
    return render_template('servico.html', servicos=servicos)

@app.route('/agendar_servico/<int:id>', methods=['POST'])
def agendar_servico(id):
    servico = Servico.query.get(id)
    data = request.form['data']
    horario = request.form['horario']

    if servico.consultor_disponivel:
        mensagem = f"Serviço '{servico.nome_solucao}' agendado para {data} às {horario}."
    else:
        mensagem = "Consultor não disponível para essa data."

    return render_template('servico.html', servicos=Servico.query.all(), mensagem=mensagem)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Criação do banco de dados dentro do contexto
    app.run(debug=True, host='0.0.0.0', port=5000)
