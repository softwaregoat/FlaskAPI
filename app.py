from flask import Flask, json, abort, jsonify, request
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


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.route('/api/put', methods=['POST'])
def put_query():
    if 'filename' in request.args and 'key' in request.args and 'value' in request.args:
        key = request.args['key']
        value = request.args['value']
        file_name1 = request.args['filename']
        file_name = FilePath + file_name1 + '.txt'
        if path.exists(file_name):
            with open(file_name, 'a') as f:
                f.write(",'" + key + "':'" + value + "'")
            f.close()
            return 'Success'
        else:
            return file_name1 + ' does not exist'
    else:
        abort(400)


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return json.dumps({'task': task[0]})


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5555)
