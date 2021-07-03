import os
from flask import Flask, render_template, url_for, redirect
from forms import AddForm, DelForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'


### SQL DATABASE SECTION ###

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


### MODELS ###

class Funcionario(db.Model):
    __tablename__ = 'funcionarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text)
    email = db.Column(db.Text)
    aniversario = db.Column(db.Text)
    
    def __init__(self, nome, email, aniversario):
        self.nome = nome
        self.email = email
        self.aniversario = aniversario
        
        
### VIEWS FUNCTIONS ###

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_funcionario():
    form = AddForm()
    
    if form.validate_on_submit():
        nome = form.nome.data
        email = form.email.data
        aniversario = form.aniversario.data
        
        novo_funcionario = Funcionario(nome, email, aniversario)
        db.session.add(novo_funcionario)
        db.session.commit()
        
        return redirect(url_for('lista_funcionarios'))
    return render_template('add.html', form=form)


@app.route('/list')
def lista_funcionarios():
    funcionarios = Funcionario.query.all()
    return render_template('list.html', funcionarios=funcionarios)

@app.route('/delete', methods=['GET', 'POST'])
def deletar_funcionario():
    form = DelForm()
    
    if form.validate_on_submit():
        try:
            id = form.id.data
            funcionario = Funcionario.query.get(id)
            db.session.delete(funcionario)
            db.session.commit()
            return redirect(url_for('lista_funcionarios'))
        except Exception:
            return redirect(url_for('error_404'))

    return render_template('delete.html', form=form)

@app.route('/404')
def error_404():
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)