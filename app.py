from flask import Flask, json, abort, jsonify, request
from werkzeug.utils import secure_filename
from os import path

app = Flask(__name__)
FilePath = './Files/'

f = open('api_key.json',)
data = json.load(f)
api_key = data['api_key']
f.close()


@app.route('/')
def hello_world():
    return 'Api works well'


@app.route('/api/<string:file_name>', methods=['GET'])
def get_query(file_name):
    key = request.args['api_key']
    if key != api_key:
        abort(404)
    file_name = FilePath + file_name + '.txt'
    if path.exists(file_name):
        result = ''
        with open(file_name) as f:
            result = f.read()
        f.close()
        if result == '':
            return 'No result', 200
        return result, 200
    else:
        return 'No exit the file', 200


@app.route('/api/uploader', methods=['GET', 'POST'])
def upload_file():
    key = request.args['api_key']
    if key != api_key:
        abort(404)
    if request.method == 'POST':
        if 'files[]' not in request.files:
            return 'request param should be files[]', 400
        files = request.files.getlist('files[]')
        for file in files:
            filename = secure_filename(file.filename)
            file.save(path.join(FilePath, filename))
        return 'files uploaded successfully', 200
    else:
        return 'It should POST', 400
   

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port=8080)
