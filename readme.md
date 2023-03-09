# Install

Clone the repository

    git clone git@github.com:kostorub/db-perfomance-test.git
    cd db-perfomance-test

Start a docker container for the Postgresql service

    docker-compose -f docker-compose/postgresql.yaml up

Use either CPython interpreter or PyPy for the best perfomance

    python3 -m venv .venv_cpython
    . ./.venv_cpython/bin/activate
    pip install pip-tools
    pip-compile
    pip-sync

For basic benchmarks use

    python3 ./src/api.py
