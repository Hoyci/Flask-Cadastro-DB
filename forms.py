from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField
from wtforms.validators import InputRequired

class AddForm(FlaskForm):
    
    nome = StringField('Nome do Funcionário: ', validators=[InputRequired()])
    email = StringField('Email do Funcionário: ', validators=[InputRequired()])
    aniversario = DateField('Data de Aniversário do Funcionário: ', validators=[InputRequired()],  format='%d-%m-%Y')
    enviar = SubmitField('Adicionar Funcionário')
    
class DelForm(FlaskForm):
    id = IntegerField('ID do funcionário para remoção: ')
    enviar = SubmitField('Remover Funcionário')