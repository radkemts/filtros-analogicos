from flask import render_template, request, redirect, url_for
from app import app
from app.controllers.filters import filter_design

@app.route('/', methods=['GET'])
def index():
    return render_template('form.html')

@app.route('/result', methods=['POST'])
def result():
    filter_result = filter_design(request)
    template = filter_result.filter_type + '-' + filter_result.approx + '.html'
    return render_template(template_name_or_list=template, result=filter_result)

@app.errorhandler(404)
@app.errorhandler(405)
def page_not_found(e):
    return redirect(url_for('index'))