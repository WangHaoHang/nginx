from flask import Flask, request, make_response

app = Flask('__name__')


@app.route(rule='/index/<name>',methods=['GET'])
def index(name):
    return make_response("<h1>Hello world!</h1")


if __name__ == '__main__':
    app.run('localhost', 8808)
