import os
from flask import Flask
from flask import redirect
from flask import request
from snitch import Snitch


def get_config_dict():
    with open('user.cfg', 'r') as f:
        return f.read().splitlines()


def setup_click():
    if not os.path.isfile('clicks.dat'):
        with open('clicks.dat', 'w') as f:
            f.write(str(0))


app = Flask(__name__)
config = get_config_dict()
setup_click()

@app.route('/snitch/<id>')
def snitch(id):
    snitch_instance = Snitch(config[0], config[1], config[2], config[3])
    snitch_instance.move(id)
    return redirect(request.headers.get('Referer'))


app.run('0.0.0.0', 8000)