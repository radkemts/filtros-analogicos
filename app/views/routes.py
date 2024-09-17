from flask import render_template, request
from app import app
from app.controllers.filtros import filtro

@app.route('/', methods=['GET'])
def index():
    return render_template('formulario.html')

@app.route('/resultado', methods=['POST'])
def resultado():
    resultado = filtro(request)
    template = resultado['filtro'] + '-' + resultado['approx'] + '.html'
    return render_template(template_name_or_list=template, resultado=resultado)