from flask import Flask, request, make_response, session, render_template
import threading

app = Flask('__name__')

app1 = Flask('__init__', template_folder=".")


@app1.before_request
def login():
    print(request.remote_addr, request.environ.get('REMOTE_PORT'), request.path)


@app1.route(rule='/test/<name>')
def test(name):
    return render_template('index.html', name=name)


@app.route(rule='/index/<name>', methods=['GET'])
def index(name):
    result = "<h1>Hello world!" + name + "</h1>"
    return make_response(result)


if __name__ == '__main__':
    t1 = threading.Thread(name='app', target=app.run, args=('localhost', 8808,))
    t2 = threading.Thread(name='app1', target=app1.run, args=('localhost', 8807,))
    # app.run('localhost', 8808)
    t1.start()
    t2.start()
