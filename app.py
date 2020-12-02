from flask import Flask, json, abort, jsonify, request
from werkzeug.utils import secure_filename
from os import path

app = Flask(__name__)
FilePath = './Files/'


@app.route('/')
def hello_world():
    return 'Api works well'


@app.route('/api/<string:file_name>', methods=['GET'])
def get_query(file_name):
    key = request.args['key']
    val = ''
    if len(key) == 0:
        abort(404)
    file_name = FilePath + file_name + '.txt'
    if path.exists(file_name):
        with open(file_name) as f:
            for line in f:
                lines = line.replace('\'', '').split(',')
                for l in lines:
                    (k, v) = l.split(':')
                    if k == key:
                        val = v
                        break
                if val != '':
                    break
        f.close()
        if val == '':
            return 'No result', 200
        return jsonify({'key': key, 'result': val}), 200
    else:
        abort(400)


@app.route('/api/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(path.join(FilePath, filename))
        return 'file uploaded successfully'
   

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port=8080)
