from flask import Flask

app = Flask(__name__)

# increase the timeout settings
import time
import signal

def timeout_handler(signum, frame):
    raise TimeoutError()

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(30) # set timeout to 30 seconds

# define the routes
@app.route('/')
def home():
    return '<h1>FLIPP</h1><p>This app allows you to detect the emotion of your text, video and audio inputs.</p>'

# disable the timeout alarm
signal.alarm(0)

if __name__ == '__main__':
    app.run(port=8000)
