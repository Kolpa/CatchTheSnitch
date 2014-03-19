import os
from praw import Reddit
from random import randrange
from flask import Flask
from flask import redirect
from flask import request

def load_raw_css():
    with open('raw.css', 'r') as f:
        return f.read()


def make_css(x, y):
    return load_raw_css().format(x, y, config[3])


def get_random_pos():
    x = randrange(0, 100, 10)
    y = randrange(0, 100, 10)
    return make_css(x, y)


def get_config_dict():
    with open('user.cfg', 'r') as f:
        return f.read().splitlines()


def load_raw_desc():
    with open('descripiton.txt', 'r') as f:
        return f.read()


def track_click():
    with open('clicks.dat', 'r+') as f:
        val = int(f.read())
        f.seek(0)
        f.write(str(val + 1))
        return val + 1


def setup_click():
    if not os.path.isfile('clicks.dat'):
        with open('clicks.dat', 'w') as f:
            f.write(str(0))


def make_desc():
    return load_raw_desc().format(track_click())


def move_snitch():
    rh = Reddit('Release the Snitch v 0.1 by Kolpa')
    rh.login(config[0], config[1])

    css = get_random_pos()
    rh.set_stylesheet(config[2], css)
    desc = make_desc()
    rh.update_settings(rh.get_subreddit(config[2]), description=desc)
    print 'the snitch has been moved'


app = Flask(__name__)
config = get_config_dict()
setup_click()

@app.route('/snitch')
def snitch():
    move_snitch()
    return redirect(request.headers.get('Referer'))

app.run('0.0.0.0', 80)