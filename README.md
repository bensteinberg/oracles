[![CircleCI](https://circleci.com/gh/bensteinberg/oracles.svg?style=svg)](https://circleci.com/gh/bensteinberg/oracles) [![codecov](https://codecov.io/gh/bensteinberg/oracles/branch/master/graph/badge.svg)](https://codecov.io/gh/bensteinberg/oracles)

This is an application for generating Big Pictures for Ben Robbins'
excellent game, [Microscope](http://www.lamemage.com/microscope/),
using the Oracles mechanism from [Microscope
Explorer](http://www.lamemage.com/microscope-explorer/).

To set up the application, install `python3-venv` if necessary, then run

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Copy `data.py.sample` to `data.py`, or create your own version. You
can then run the application with `FLASK_ENV=development python
server.py`. Visit it at
[http://127.0.0.1:5000/oracles](http://127.0.0.1:5000/oracles), which
will redirect you to a random roll of six six-sided dice for a random
oracle. Adding an oracle (or substring) to the base URL, e.g.
[http://127.0.0.1:5000/oracles/angst](http://127.0.0.1:5000/oracles/angst),
will redirect you to a random roll for that oracle. The underlying API
behaves the same way, and can be viewed at
[http://127.0.0.1:5000/oracles/api/v1](http://127.0.0.1:5000/oracles/api/v1).

You can also run a big picture generator on the command line with
`python oracles.py`.

If you're hacking on this code, you can run the tests with `pytest`;
use `flake8 --exclude=env/` to keep it clean. If you add Python
packages, add them to `requirements.in` and run `pip-compile
--generate-hashes` to update `requirements.txt`.

(Lame Mage has an [online
version](http://www.lamemage.com/oracles/) of the
Oracles, announced
[here](http://arsludi.lamemage.com/index.php/753/oracles-for-everyone/).)
