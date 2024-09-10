from flask import render_template, request
from app import app
from app.controllers.filtros import calcula as calc

@app.route('/', methods=['GET'])
def index():
    return render_template('formulario.html')

@app.route('/resultado', methods=['POST'])
def calcula():
    resultado = calc(request)
    return render_template('resultado.html', resultado=resultado)