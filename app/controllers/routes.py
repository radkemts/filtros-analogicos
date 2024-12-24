from flask import render_template, request, jsonify
from app import app
from app.controllers.filters import filter_design

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    filter_result = filter_design(request)

    if hasattr(filter_result, 'status') and filter_result.status == 'warning':
        return jsonify(filter_result)
    else:
        template = filter_result.filter_type + '-' + filter_result.approx + '.html'
        return jsonify({'status': 'success', 'template': render_template(template, result=filter_result)})