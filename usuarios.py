from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'Lucasfff'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'

db = SQLAlchemy(app)


class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    funcao = db.Column(db.String(100))

    def __init__(self, nome, funcao):
        self.nome = nome
        self.funcao = funcao


@app.route('/')
def index():
    titulo = 'Lista de Usuários'
    return render_template('users.html', titulo=titulo, usuarios=Usuarios.query.all())


@app.route('/novo')
def novo():
    titulo = 'Adicionar novos Usuários'
    return render_template('novo.html', titulo=titulo)


@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form.get('nome')
    funcao = request.form.get('funcao')

    user_novo = Usuarios(nome=nome, funcao=funcao)
    db.session.add(user_novo)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    titulo = 'Atualizando Usuário'
    user = Usuarios.query.filter_by(id=id).first()
    return render_template('editar.html', titulo=titulo, user=user)


@app.route('/atualizar', methods=['POST', ])
def atualizar():
    user = Usuarios.query.filter_by(id=request.form['id']).first()
    user.nome = request.form['nome']
    user.funcao = request.form['funcao']

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    Usuarios.query.filter_by(id=id).delete()
    db.session.commit()

    flash('Usuário Deletado')
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
