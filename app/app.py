from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, It is not working as expected what to do next'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
