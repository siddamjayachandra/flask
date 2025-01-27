from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
    # Get the current date and time
    current_datetime = datetime.now().strftime("%A, %B %d, %Y %I:%M:%S %p")
    return f"Hello, Today is {current_datetime}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

