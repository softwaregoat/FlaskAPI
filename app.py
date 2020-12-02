from flask import Flask, json, abort, jsonify, request
from werkzeug.utils import secure_filename
import os
from os import path

app = Flask(__name__)
FilePath = './Files/'

f = open('api_key.json',)
data = json.load(f)
f.close()


@app.route('/')
def hello_world():
    return 'Api works well'


# fetch file with get
@app.route('/api/<string:file_name>', methods=['GET'])
def get_query(file_name):
    key = request.args['api_key']
    if key != data['api_key']:
        return 'Invalid api_key', 400
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


# upload files with post
@app.route('/api/uploader', methods=['GET', 'POST'])
def upload_files():
    key = request.args['api_key']
    if key != data['api_key']:
        return 'Invalid api_key', 400
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
   

# delete file with post
@app.route('/api/delete/<string:file_name>', methods=['GET', 'POST'])
def post_delete_file(file_name):
    key = request.args['api_key']
    if key != data['api_key']:
        return 'Invalid api_key', 200
    if request.method == 'POST':
        file_name = FilePath + file_name + '.txt'
        if path.exists(file_name):
            os.remove(file_name)
            return 'Successfully Deleted for the file', 200
        else:
            return 'No exit the file', 200
    else:
        return 'It should POST', 400
    
        
# delete all files with post
@app.route('/api/delete', methods=['GET', 'POST'])
def post_delete_all():
    key = request.args['api_key']
    if key != data['api_key']:
        return 'Invalid api_key', 200
    if request.method == 'POST':
        for filename in os.listdir(FilePath):
            file_path = os.path.join(FilePath, filename)
            try:
                os.remove(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        
        return 'Successfully Deleted for all files', 200
    else:
        return 'It should POST', 400


# update api key
@app.route('/api/update', methods=['GET', 'POST'])
def post_update_api_key():
    key = request.args['api_key']
    if key != data['api_key']:
        return 'Invalid api_key', 200
    if request.method == 'POST':
        new_key = request.args['new_key']
        data['api_key'] = new_key
        with open('api_key.json', 'w') as outfile:
            json.dump(data, outfile)
        return 'Successfully updated for api key', 200
    else:
        return 'It should POST', 400
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port=8080)
