from flask import (Flask,
                   Blueprint,
                   request,
                   render_template,
                   redirect,
                   url_for,
                   jsonify)
from oracles import Oracle, oracles
from random import choice

bp = Blueprint('oracle', __name__,
               template_folder='templates',
               static_folder='static')


@bp.route('/')
def hello():
    return render_template('index.html')


@bp.route('/api/v1')
def random_all():
    o = choice([o['name'] for o in oracles])
    d = [choice(range(0, 6)) + 1 for _ in range(0, 6)]
    return oracle_redirect(o, d)


@bp.route('/api/v1/<o>')
def api_random_roll(o):
    try:
        res = Oracle(o)
        return oracle_redirect(o, res.dice)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@bp.route('/api/v1/<o>/<d1>/<d2>/<d3>/<d4>/<d5>/<d6>')
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


@bp.route('/<o>/<d1>/<d2>/<d3>/<d4>/<d5>/<d6>')
def oracle(o, d1, d2, d3, d4, d5, d6):
    roll = [r for r in map(int, [d1, d2, d3, d4, d5, d6])]
    res = Oracle(o, roll)
    return render_template('oracle.html',
                           o=o,
                           text=res.text,
                           oracles=oracles,
                           # this is clunky
                           path=request.path.replace('/oracles/',
                                                     '/oracles/api/v1/'))


@bp.route('/<o>')
def random_roll(o):
    res = Oracle(o)
    d = res.dice
    return redirect(url_for('oracle.oracle',
                            o=res.oracle,
                            d1=d[0],
                            d2=d[1],
                            d3=d[2],
                            d4=d[3],
                            d5=d[4],
                            d6=d[5]))


def oracle_redirect(o, d):
    return redirect(url_for('oracle.oracle_api',
                            o=o,
                            d1=d[0],
                            d2=d[1],
                            d3=d[2],
                            d4=d[3],
                            d5=d[4],
                            d6=d[5]))


app = Flask(__name__)
app.register_blueprint(bp, url_prefix='/oracles')


if __name__ == '__main__':
    app.run()
