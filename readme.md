# Install

Use either CPython interpreter or PyPy for the best perfomance

    python3 -m venv .venv_cpython
    . ./.venv_cpython/bin/activate
    pip install pip-tools
    pip-compile
    pip-sync

For basic benchmarks use

    python3 ./src/api.py
