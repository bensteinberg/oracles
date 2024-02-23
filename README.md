This is an application for generating Big Pictures for Ben Robbins'
excellent game, [Microscope](http://www.lamemage.com/microscope/),
using the Oracles mechanism from [Microscope
Explorer](http://www.lamemage.com/microscope-explorer/).

To set up the application, [install
Poetry](https://python-poetry.org/docs/#installation), then run

```
poetry install
```

Copy `oracles/data_sample.py` to `oracles/data.py`, or create your own
version. You can then run the application with `FLASK_DEBUG=1 poetry run python oracles/server.py`. Visit it at
[http://127.0.0.1:5000/oracles](http://127.0.0.1:5000/oracles), which
will redirect you to a random roll of six six-sided dice for a random
oracle. Adding an oracle (or substring) to the base URL, e.g.
[http://127.0.0.1:5000/oracles/angst](http://127.0.0.1:5000/oracles/angst),
will redirect you to a random roll for that oracle. The underlying API
behaves the same way, and can be viewed at
[http://127.0.0.1:5000/oracles/api/v1](http://127.0.0.1:5000/oracles/api/v1).

You can also run a big picture generator on the command line; run
`ORACLES=oracles.data poetry run oracles` to generate a Big
Picture. Try `oracles --help` for options.

You can also run the web application using Docker; running
`docker-compose up -d` will make it available at [http://127.0.0.1:8001/oracles](http://127.0.0.1:8001/oracles). Run
`docker-compose down` to stop the containers.

If you're hacking on this code, you can run the tests with `poetry run
pytest`. Use `poetry run flake8` to keep it clean. You may have to run `poetry run playwright install` to install the browsers for Playwright. For the browser tests to work, the application has to be running on localhost (TODO: get the live_server fixture set up properly). Add Python packages with `poetry add <package>` or `poetry add --group dev <package>`, as appropriate. After changing non-dev packages, update the conventional requirements file with `poetry export -o oracles/requirements.txt`.

(Lame Mage has an [online
version](http://www.lamemage.com/oracles/) of the
Oracles, announced
[here](http://arsludi.lamemage.com/index.php/753/oracles-for-everyone/).)
