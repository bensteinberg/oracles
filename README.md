This is an application for generating Big Pictures for Ben Robbins'
excellent game, Microscope, using the Oracles mechanism from
_Microscope Explorer_.

To set up the application, install `python3-venv` if necessary, then run

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Copy `data.py.sample` to `data.py`, or create your own version. You
can then run the application with `python server.py` or
`FLASK_ENV=development python server.py`.

If you're hacking on this code, you can run the tests with `pytest`;
use `flake8 --exclude=env/` to keep it clean. If you add Python
packages, add them to `requirements.in` and run `pip-compile
--generate-hashes` to update `requirements.txt`.
