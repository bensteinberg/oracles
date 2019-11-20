from flask import (Flask,
                   Blueprint,
                   request,
                   render_template,
                   redirect,
                   url_for,
                   jsonify,
                   current_app)
from oracles import Oracle, oracles
from random import choice

bp = Blueprint('oracle', __name__,
               template_folder='templates',
               static_folder='static')


@bp.route('/')
def random_oracle():
    o = choice([o['name'] for o in oracles])
    return redirect(url_for('oracle.random_roll', o=o))


@bp.route('/api/v1')
def api_random_oracle():
    o = choice([o['name'] for o in oracles])
    d = [choice(range(0, 6)) + 1 for _ in range(0, 6)]
    return api_redirect(o, d)


@bp.route('/api/v1/<o>')
def api_random_roll(o):
    try:
        res = Oracle(o)
        return api_redirect(o, res.dice)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@bp.route('/api/v1/<o>/<d1>/<d2>/<d3>/<d4>/<d5>/<d6>')
def api(o, d1, d2, d3, d4, d5, d6):
    roll = [r for r in map(int, [d1, d2, d3, d4, d5, d6])]
    try:
        res = Oracle(o, roll)
        return jsonify({'oracle': res.oracle,
                        'text': res.text,
                        'dice': res.dice,
                        'trend': res.trend,
                        'impact': res.impact,
                        'elements': [
                            res.element_a,
                            res.element_b
                        ],
                        'api_uri': request.url,
                        'path': request.path.replace('/api/v1', '')})
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


def api_redirect(o, d):
    if current_app.env == 'production':
        dest = url_for('oracle.api',
                       o=o,
                       d1=d[0],
                       d2=d[1],
                       d3=d[2],
                       d4=d[3],
                       d5=d[4],
                       d6=d[5],
                       _external=True,
                       _scheme='https')
    else:
        dest = url_for('oracle.api',
                       o=o,
                       d1=d[0],
                       d2=d[1],
                       d3=d[2],
                       d4=d[3],
                       d5=d[4],
                       d6=d[5])
    return redirect(dest)


@bp.errorhandler(ValueError)
def handle_invalid_usage(error):
    return render_template('error.html', error=error)


app = Flask(__name__)
app.register_blueprint(bp, url_prefix='/oracles')


if __name__ == '__main__':
    app.run()
