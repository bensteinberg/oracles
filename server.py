from flask import (Flask,
                   request,
                   render_template,
                   redirect,
                   url_for,
                   jsonify,
                   send_from_directory)
from oracles import Oracle, oracles
from random import choice
import os

app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/api/v1')
def random_all():
    o = choice([o['name'] for o in oracles])
    d = [choice(range(0, 6)) + 1 for _ in range(0, 6)]
    return oracle_redirect(o, d)


@app.route('/api/v1/<o>')
def api_random_roll(o):
    try:
        res = Oracle(o)
        return oracle_redirect(o, res.dice)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/v1/<o>/<d1>/<d2>/<d3>/<d4>/<d5>/<d6>')
def oracle_api(o, d1, d2, d3, d4, d5, d6):
    roll = [r for r in map(int, [d1, d2, d3, d4, d5, d6])]
    try:
        res = Oracle(o, roll)
        return jsonify({'oracle': res.oracle,
                        'text': res.text,
                        'dice': res.dice,
                        'api_uri': request.url,
                        'path': request.path})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/<o>/<d1>/<d2>/<d3>/<d4>/<d5>/<d6>')
def oracle(o, d1, d2, d3, d4, d5, d6):
    roll = [r for r in map(int, [d1, d2, d3, d4, d5, d6])]
    res = Oracle(o, roll)
    path = '/%s/%s' % (o, '/'.join(map(str, roll)))
    return render_template('oracle.html', o=o, text=res.text, path=path)


@app.route('/<o>')
def random_roll(o):
    res = Oracle(o)
    d = res.dice
    return redirect(url_for('oracle',
                            o=res.oracle,
                            d1=d[0],
                            d2=d[1],
                            d3=d[2],
                            d4=d[3],
                            d5=d[4],
                            d6=d[5]))


def oracle_redirect(o, d):
    return redirect(url_for('oracle_api',
                            o=o,
                            d1=d[0],
                            d2=d[1],
                            d3=d[2],
                            d4=d[3],
                            d5=d[4],
                            d6=d[5]))


if __name__ == '__main__':
    app.run()
